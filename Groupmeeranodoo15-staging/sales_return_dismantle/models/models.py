# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.tools import float_compare, float_round
from odoo.exceptions import UserError


class DismantleProcess(models.Model):
    _name = 'dismantle.process'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Dismantle Process'
    _order = 'id desc'

    name = fields.Char('Reference', copy=False, readonly=True, default=lambda x: _('New'))
    product_id = fields.Many2one(
        'product.product', 'Product', check_company=True,
        domain="[('type', 'in', ['product', 'consu']), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        required=True, states={'done': [('readonly', True)], 'transferred': [('readonly', True)]})
    company_id = fields.Many2one(
        'res.company', 'Company',
        default=lambda s: s.env.company,
        required=True, index=True, states={'done': [('readonly', True)], 'transferred': [('readonly', True)]})
    user_id = fields.Many2one('res.users', string='User', index=True, tracking=True, default=lambda self: self.env.user,
                              check_company=True)
    product_qty = fields.Float(
        'Quantity', default=1.0,
        required=True, states={'done': [('readonly', True)], 'transferred': [('readonly', True)]})
    product_uom_id = fields.Many2one(
        'uom.uom', 'Unit of Measure',
        required=True, states={'done': [('readonly', True)], 'transferred': [('readonly', True)]})
    process = fields.Selection(selection=[
        ('scrap', 'Scrap'),
        ('dismantle', 'Dismantle'),
        ('good_condition', 'Good Condition'),
        ('repair', 'Repair'),
        ('resell', 'Resell'),
    ], string='Process', copy=False, default='repair', states={'draft': [('readonly', False)]}, readonly=True)
    scrap_location = fields.Many2one('stock.location', string='Scrap Location', check_company=True, readonly=True,
                                     states={'draft': [('readonly', False)]},
                                     domain="[('scrap_location','=',True), ('company_id', '=', company_id)]")
    repair_location = fields.Many2one('stock.location', string='Repair Location', check_company=True, readonly=True,
                                      states={'draft': [('readonly', False)]},
                                      domain="[('repair_location','=',True), ('company_id', '=', company_id)]")
    dismantle_location = fields.Many2one('stock.location', string='Dismantle Location', check_company=True,
                                         readonly=True,
                                         states={'draft': [('readonly', False)]},
                                         domain="[('dismantle_location','=',True), ('company_id', '=', company_id)]")
    scrap_id = fields.Many2one('stock.scrap', string='Scrap', copy=False)
    sale_return_id = fields.Many2one('sales.return', string='Return Reference', ondelete='cascade',
                                     index=True, copy=False)
    picking_id_status = fields.Selection(string='Status', related="sale_return_id.picking_id_status", copy=False,
                                         readonly=True, store=True)
    dismantle_operation_type = fields.Many2one('stock.picking.type', 'Dismantle Operation Type', readonly=True,
                                               states={'draft': [('readonly', False)]},
                                               domain="[('code','=','internal'), ('company_id', '=', company_id), ('default_location_dest_id', '=', dismantle_location)]")
    dismantle_picking_id = fields.Many2one('stock.picking', string='Dismantle Internal Transfer', copy=False)
    repair_components = fields.One2many('repair.components', 'dismantle_process_id', string='Repair Components',
                                        readonly=True, states={'draft': [('readonly', False)]}, copy=False,
                                        auto_join=True)

    repair_operation_type = fields.Many2one('stock.picking.type', 'Repair Operation Type', readonly=True,
                                            states={'draft': [('readonly', False)]},
                                            domain="[('code','=','internal'), ('company_id', '=', company_id), ('default_location_dest_id', '=', repair_location)]")
    repair_picking_id = fields.Many2one('stock.picking', string='Repair Internal Transfer', copy=False)
    repair_delivery_id = fields.Many2one('stock.picking', string='Repair Delivery', copy=False)

    bom_id = fields.Many2one(
        'mrp.bom', 'Bill of Material',
        domain="""[
            '|',
                ('product_id', '=', product_id),
                '&',
                    ('product_tmpl_id.product_variant_ids', '=', product_id),
                    ('product_id','=',False),
            ('type', '=', 'normal'),
            '|',
                ('company_id', '=', company_id),
                ('company_id', '=', False)
            ]
    """,
        states={'done': [('readonly', True)]}, check_company=True)
    lot_id = fields.Many2one(
        'stock.production.lot', 'Lot/Serial Number',
        domain="[('product_id', '=', product_id), ('company_id', '=', company_id)]", check_company=True,
        states={'done': [('readonly', True)], 'transferred': [('readonly', True)]}, help="Lot/Serial Number of the product to dismantle.")
    has_tracking = fields.Selection(related='product_id.tracking', readonly=True)
    location_id = fields.Many2one(
        'stock.location', 'Source Location',
        domain="[('usage','=','internal'), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        check_company=True,
        required=True, states={'done': [('readonly', True)], 'transferred': [('readonly', True)]},
        help="Location where the product you want to dismantle is.")
    location_dest_id = fields.Many2one(
        'stock.location', 'Destination Location',
        domain="[('usage','=','internal'), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        check_company=True,
        required=True, states={'done': [('readonly', True)], 'transferred': [('readonly', True)]},
        help="Location where you want to send the components resulting from the dismantle order.")
    consume_line_ids = fields.One2many(
        'stock.move', 'consume_dismantle_id', readonly=True,
        string='Consumed Disassembly Lines')
    produce_line_ids = fields.One2many(
        'stock.move', 'produce_dismantle_id', readonly=True,
        string='Processed Disassembly Lines')
    state = fields.Selection([
        ('draft', 'Draft'), ('transferred', 'Transferred'), ('done', 'Done'), ('cancel', 'Cancel'),
    ], string='Status', default='draft')

    dismantle_product_lines = fields.One2many('dismantle.product.line', 'dismantle_process_id',
                                              string='Resulted Products',
                                              states={'cancel': [('readonly', True)], 'done': [('readonly', True)]},
                                              copy=True,
                                              auto_join=True)

    @api.onchange('product_id', 'process')
    def _onchange_product_id(self):
        if self.product_id and self.process == 'dismantle':
            self.bom_id = self.env['mrp.bom']._bom_find(self.product_id, company_id=self.company_id.id)[self.product_id]
            if not self.product_uom_id:
                self.product_uom_id = self.product_id.uom_id.id

    @api.onchange('bom_id')
    def _onchange_bom_id(self):
        if not self.product_id and self.bom_id:
            self.product_id = self.bom_id.product_id or self.bom_id.product_tmpl_id.product_variant_ids[0]
        self.dismantle_product_lines = [(2, move.id) for move in
                                        self.dismantle_product_lines.filtered(lambda m: m.bom_line_id)]

    @api.constrains('product_qty')
    def _check_qty(self):
        for record in self:
            if record.product_qty <= 0:
                raise ValueError(_('Dismantle Order product quantity has to be strictly positive.'))

    def _generate_consume_moves(self):
        moves = self.env['stock.move']
        for record in self:
            location_dest_id = record.product_id.with_company(record.company_id).property_stock_production
            warehouse = location_dest_id.warehouse_id
            move = self.env['stock.move'].create(
                {
                    'name': record.name,
                    'date': record.create_date,
                    'product_id': record.product_id.id,
                    'product_uom_qty': record.product_qty,
                    'product_uom': record.product_uom_id.id,
                    'procure_method': 'make_to_stock',
                    'location_dest_id': location_dest_id.id,
                    'location_id': record.dismantle_location.id,
                    'warehouse_id': warehouse.id,
                    'consume_dismantle_id': self.id,
                    'company_id': self.company_id.id,
                }
            )
            moves += move
        return moves

    def _generate_produce_moves(self):
        moves = self.env['stock.move']
        for record in self:
            for line in record.dismantle_product_lines:
                location_id = record.product_id.with_company(record.company_id).property_stock_production
                move = self.env['stock.move'].create(
                    {
                        'name': record.name,
                        'date': record.create_date,
                        'product_id': line.product_id.id,
                        'product_uom_qty': line.product_qty,
                        'product_uom': line.product_uom_id.id,
                        'procure_method': 'make_to_stock',
                        'location_dest_id': line.destination_location.id,
                        'location_id': location_id.id,
                        'warehouse_id': line.destination_location.warehouse_id.id,
                        'produce_dismantle_id': self.id,
                        'dismantle_product_line_id': line.id,
                        'company_id': self.company_id.id,
                    }
                )
                moves += move
        return moves

    def move_to_scrap(self):
        for line in self.dismantle_product_lines.filtered(lambda m: m.scrap and m.scrap_location_id):
            scrap = self.env['stock.scrap'].create({
                'product_id': line.product_id.id,
                'product_uom_id': line.product_uom_id.id,
                'scrap_qty': line.product_qty,
                'lot_id': line.lot_id.id,
                'location_id': line.destination_location.id,
                'scrap_location_id': line.scrap_location_id.id,
                'company_id': line.company_id.id,
                'dismantle_process_id': self.id,
            })
            scrap.action_validate()

    def action_view_dismantle_scrap(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("stock.action_stock_scrap")
        scraps = self.env['stock.scrap'].search([('dismantle_process_id', '=', self.id)])
        action['domain'] = [('id', 'in', scraps.ids)]
        action['context'] = dict(self._context, create=False)
        return action

    def action_dismantle(self):
        self.ensure_one()
        self._check_company()
        if self.product_id.tracking != 'none' and not self.lot_id.id:
            raise UserError(_('You should provide a lot number for the final product.'))
        consume_moves = self._generate_consume_moves()
        consume_moves._action_confirm()
        produce_moves = self._generate_produce_moves()
        produce_moves._action_confirm()

        for consume_move in consume_moves:
            if consume_move.has_tracking != 'none':
                self.env['stock.move.line'].create({
                    'move_id': consume_move.id,
                    'lot_id': self.lot_id.id,
                    'qty_done': consume_move.product_uom_qty,
                    'product_id': consume_move.product_id.id,
                    'product_uom_id': consume_move.product_uom.id,
                    'location_id': consume_move.location_id.id,
                    'location_dest_id': consume_move.location_dest_id.id,
                })
            else:
                consume_move.quantity_done = consume_move.product_uom_qty

        # TODO: Will fail if user do more than one unbuild with lot on the same MO. Need to check what other unbuild has aready took
        for move in produce_moves:
            if move.has_tracking != 'none':
                self.env['stock.move.line'].create(
                    {
                        'move_id': move.id,
                        'lot_id': move.dismantle_product_line_id.lot_id.id,
                        'qty_done': move.product_uom_qty,
                        'product_id': move.product_id.id,
                        'product_uom_id': move.product_uom_id.id,
                        'location_id': move.location_id.id,
                        'location_dest_id': move.location_dest_id.id,
                    })
            else:
                move.quantity_done = float_round(move.product_uom_qty, precision_rounding=move.product_uom.rounding)
        consume_moves._action_done()
        produce_moves._action_done()
        produced_move_line_ids = produce_moves.mapped('move_line_ids').filtered(lambda ml: ml.qty_done > 0)
        consume_moves.mapped('move_line_ids').write({'produce_line_ids': [(6, 0, produced_move_line_ids.ids)]})
        self.move_to_scrap()
        return self.write({'state': 'done'})

    def action_validate(self):
        self.ensure_one()
        if self.process == 'dismantle':
            precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
            available_qty = self.env['stock.quant']._get_available_quantity(self.product_id, self.dismantle_location, self.lot_id,
                                                                            strict=True)
            unbuild_qty = self.product_uom_id._compute_quantity(self.product_qty, self.product_id.uom_id)
            if float_compare(available_qty, unbuild_qty, precision_digits=precision) >= 0:
                return self.action_dismantle()
            else:
                raise UserError(_("Insufficient quantity to dismantle product: %s")
                                % (self.product_id.display_name)
                                )
        if self.process == 'repair':
            stock_picking = self.env['stock.picking'].create({
                # 'move_lines': [],
                'picking_type_id': self.sale_return_id.picking_type_id.return_picking_type_id.id,
                'state': 'draft',
                'origin': _("Delivery - %s") % self.name,
                'location_id': self.repair_location.id,
                'location_dest_id': self.sale_return_id.location_id.id,
                'sales_return_qc_repair_delivery_id': self.id,
                'partner_id': self.sale_return_id.partner_id.id,
            })
            if self.product_qty:
                stock_move_line = self.env['stock.move.line'].create(
                    {
                        'picking_id': stock_picking.id,
                        'company_id': self.company_id.id,
                        'product_id': self.product_id.id,
                        'product_uom_id': self.product_uom_id.id,
                        # 'product_uom_qty': self.product_qty,
                        'qty_done': self.product_qty,
                        'lot_id': self.lot_id.id,
                        'location_id': stock_picking.location_id.id,
                        'location_dest_id': stock_picking.location_dest_id.id,
                    })
            for line in self.repair_components:
                if line.product_uom_qty:
                    stock_move_line = self.env['stock.move.line'].create(
                        {
                            'picking_id': stock_picking.id,
                            'company_id': line.company_id.id,
                            'product_id': line.product_id.id,
                            'product_uom_id': line.product_uom.id,
                            # 'product_uom_qty': line.product_uom_qty,
                            'qty_done': line.product_uom_qty,
                            'lot_id': line.lot_id.id,
                            'location_id': stock_picking.location_id.id,
                            'location_dest_id': stock_picking.location_dest_id.id,
                        })
            # stock_picking.action_confirm()
            # stock_picking.action_assign()
            stock_picking.button_validate()
            if stock_picking:
                self.write({'repair_delivery_id': stock_picking.id,
                            'state': 'done'})

    @api.model
    def create(self, vals):
        if not vals.get('name') or vals['name'] == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('dismantle.process') or _('New')
        return super(DismantleProcess, self).create(vals)

    @api.ondelete(at_uninstall=False)
    def _unlink_except_done(self):
        if 'done' in self.mapped('state'):
            raise UserError(_("You cannot delete a dismantle order if the state is 'Done'."))

    def action_cancel(self):
        for record in self:
            record.state = 'cancel'

    def action_set_to_draft(self):
        for record in self:
            record.state = 'draft'

    def _get_dismantle_product_line_values(self):
        moves = []
        for record in self:
            if not record.bom_id:
                continue
            factor = record.product_uom_id._compute_quantity(record.product_qty,
                                                             record.bom_id.product_uom_id) / record.bom_id.product_qty
            boms, lines = record.bom_id.explode(record.product_id, factor,
                                                picking_type=record.bom_id.picking_type_id)
            for bom_line, line_data in lines:
                if bom_line.child_bom_id and bom_line.child_bom_id.type == 'phantom' or \
                        bom_line.product_id.type not in ['product', 'consu']:
                    continue
                moves.append(record._get_move_raw_values(
                    bom_line.product_id,
                    line_data['qty'],
                    bom_line.product_uom_id,
                    bom_line
                ))
        return moves

    def _get_move_raw_values(self, product_id, product_uom_qty, product_uom, bom_line=False):
        data = {
            'bom_line_id': bom_line.id if bom_line else False,
            'product_id': product_id.id,
            'product_qty': product_uom_qty,
            'product_uom_id': product_uom.id,
            'company_id': self.company_id.id,
            'user_id': self.user_id.id,
            'state': self.state,
            'destination_location': self.location_dest_id.id
        }
        return data

    @api.onchange('bom_id', 'product_id', 'product_qty', 'product_uom_id')
    def _onchange_dismantle_line(self):
        if not self.bom_id and not self._origin.product_id:
            return
        # Clear dismantle line if we are changing the product. In case of creation (self._origin is empty),
        # we need to avoid keeping incorrect lines, so clearing is necessary too.
        if self.product_id != self._origin.product_id:
            self.dismantle_product_lines = [(5,)]
        if self.bom_id and self.product_id and self.product_qty > 0:
            # keep manual entries
            list_move_raw = [(4, move.id) for move in
                             self.dismantle_product_lines.filtered(lambda m: not m.bom_line_id)]
            moves_raw_values = self._get_dismantle_product_line_values()
            move_raw_dict = {move.bom_line_id.id: move for move in
                             self.dismantle_product_lines.filtered(lambda m: m.bom_line_id)}
            for move_raw_values in moves_raw_values:
                if move_raw_values['bom_line_id'] in move_raw_dict:
                    # update existing entries
                    list_move_raw += [(1, move_raw_dict[move_raw_values['bom_line_id']].id, move_raw_values)]
                else:
                    # add new entries
                    list_move_raw += [(0, 0, move_raw_values)]
            self.dismantle_product_lines = list_move_raw
        else:
            self.dismantle_product_lines = [(2, move.id) for move in
                                            self.dismantle_product_lines.filtered(lambda m: m.bom_line_id)]

    @api.onchange('process')
    def set_dest_source_location_id(self):
        for record in self:
            if record.process == 'scrap':
                record.scrap_location = self.env['stock.location'].search([('company_id', '=', record.company_id.id),
                                                                           ('scrap_location', '=', True)], limit=1)
            if record.process == 'dismantle':
                record.dismantle_location = self.env['stock.location'].search(
                    [('company_id', '=', record.company_id.id),
                     ('dismantle_location', '=', True)], limit=1)
            if record.process == 'repair':
                record.repair_location = self.env['stock.location'].search([('company_id', '=', record.company_id.id),
                                                                            ('repair_location', '=', True)], limit=1)
            # if record.process == 'resell':
            #     record.location_dest_id = self.env['stock.location'].search([('company_id', '=', record.company_id.id),
            #                                                                  ('resell_location', '=', True)], limit=1)

    @api.onchange('dismantle_location')
    def load_dismantle_operation_type(self):
        for record in self:
            if record.dismantle_location:
                record.dismantle_operation_type = self.env['stock.picking.type'].search([
                    ('code', '=', 'internal'),  ('company_id', '=', record.company_id.id),
                    ('default_location_dest_id', '=', record.dismantle_location.id)], limit=1).id

    # --- SCRAP START ---
    def action_view_scrap(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("stock.action_stock_scrap")
        scraps = self.env['stock.scrap'].search([('sales_return_qc_id', '=', self.id)])
        action['domain'] = [('id', 'in', scraps.ids)]
        action['context'] = dict(self._context, create=False)
        return action

    def scrap_product(self):
        for line in self:
            scrap = self.env['stock.scrap'].create({
                'product_id': line.product_id.id,
                'product_uom_id': line.product_uom_id.id,
                'scrap_qty': line.product_qty,
                'lot_id': line.lot_id.id,
                'location_id': self.location_id.id,
                'scrap_location_id': self.scrap_location.id,
                'company_id': line.company_id.id,
                'sales_return_qc_id': self.id,
            })
            scrap.action_validate()
        self.write({
            'state': 'done',
            'scrap_id': scrap.id
        })
    # --- SCRAP END ---

    # Dismantle - Start

    def dismantle_product(self):
        for record in self:
            stock_picking = self.env['stock.picking'].create({
                # 'move_lines': [],
                'picking_type_id': record.dismantle_operation_type.id,
                'state': 'draft',
                'origin': _("Dismantle doc - %s") % record.name,
                'location_id': record.location_id.id,
                'location_dest_id': record.dismantle_location.id,
                'sales_return_qc_dismantle_id': record.id,
            })
            if record.product_qty:
                stock_move_line = self.env['stock.move.line'].create(
                    {
                        'picking_id': stock_picking.id,
                        'company_id': record.company_id.id,
                        'product_id': record.product_id.id,
                        'product_uom_id': record.product_uom_id.id,
                        # 'product_uom_qty': record.product_qty,
                        'qty_done': record.product_qty,
                        'lot_id': record.lot_id.id,
                        'location_id': stock_picking.location_id.id,
                        'location_dest_id': stock_picking.location_dest_id.id,

                    })
            # stock_picking.action_confirm()
            # stock_picking.action_assign()
            stock_picking.button_validate()
            if stock_picking:
                record._onchange_product_id()
                record._onchange_dismantle_line()
                record.write({
                    'state': 'transferred',
                    'dismantle_picking_id': stock_picking.id
                })

    def action_view_dismantle_transfer(self):
        action = self.env["ir.actions.actions"]._for_xml_id("stock.action_picking_tree_all")

        if self.dismantle_picking_id:
            form_view = [(self.env.ref('stock.view_picking_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = self.dismantle_picking_id.id
        # Prepare the context.
        picking_id = self.dismantle_picking_id.filtered(lambda l: l.picking_type_id.code == 'internal')
        if picking_id:
            picking_id = picking_id[0]
        else:
            picking_id = self.dismantle_picking_id[0]
        return action

    # Dismantle - End

    # Repair - Start

    def repair_product(self):
        for record in self:
            stock_picking = self.env['stock.picking'].create({
                # 'move_lines': [],
                'picking_type_id': record.repair_operation_type.id,
                'state': 'draft',
                'origin': _("Repair doc - %s") % record.name,
                'location_id': record.location_id.id,
                'location_dest_id': record.repair_location.id,
                'sales_return_qc_repair_id': record.id,
            })

            if record.product_qty:
                stock_move_line = self.env['stock.move.line'].create(
                    {
                        'picking_id': stock_picking.id,
                        'company_id': record.company_id.id,
                        'product_id': record.product_id.id,
                        'product_uom_id': record.product_uom_id.id,
                        # 'product_uom_qty': record.product_qty,
                        'qty_done': record.product_qty,
                        'lot_id': record.lot_id.id,
                        'location_id': stock_picking.location_id.id,
                        'location_dest_id': stock_picking.location_dest_id.id,

                    })

            for line in record.repair_components:
                if line.product_uom_qty:
                    stock_move_line = self.env['stock.move.line'].create(
                        {
                            'picking_id': stock_picking.id,
                            'company_id': line.company_id.id,
                            'product_id': line.product_id.id,
                            'product_uom_id': line.product_uom.id,
                            # 'product_uom_qty': line.product_uom_qty,
                            'qty_done': line.product_uom_qty,
                            'lot_id': line.lot_id.id,
                            'location_id': stock_picking.location_id.id,
                            'location_dest_id': stock_picking.location_dest_id.id,
                        })

            # stock_picking.action_confirm()
            # stock_picking.action_assign()
            stock_picking.button_validate()
            if stock_picking:
                record.write({
                    'state': 'transferred',
                    'repair_picking_id': stock_picking.id
                })

    def action_view_repair(self):
        action = self.env["ir.actions.actions"]._for_xml_id("stock.action_picking_tree_all")

        if self.repair_picking_id:
            form_view = [(self.env.ref('stock.view_picking_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = self.repair_picking_id.id
        # Prepare the context.
        picking_id = self.repair_picking_id.filtered(lambda l: l.picking_type_id.code == 'internal')
        if picking_id:
            picking_id = picking_id[0]
        else:
            picking_id = self.repair_picking_id[0]
        return action

    def action_view_delivery(self):
        action = self.env["ir.actions.actions"]._for_xml_id("stock.action_picking_tree_all")

        if self.repair_delivery_id:
            form_view = [(self.env.ref('stock.view_picking_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = self.repair_delivery_id.id
        # Prepare the context.
        picking_id = self.repair_delivery_id.filtered(lambda l: l.picking_type_id.code == 'outgoing')
        if picking_id:
            picking_id = picking_id[0]
        else:
            picking_id = self.repair_delivery_id[0]
        return action
    # Repair - End


class DismantleProductLine(models.Model):
    _name = 'dismantle.product.line'
    _description = 'Dismantle Product Line'
    _order = 'dismantle_process_id, id'
    _check_company_auto = True

    dismantle_process_id = fields.Many2one('dismantle.process', string='Dismantle Reference', required=True,
                                           ondelete='cascade',
                                           index=True, copy=False)
    product_id = fields.Many2one(
        'product.product', 'Product', check_company=True,
        domain="[('type', 'in', ['product', 'consu']), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        required=True, states={'done': [('readonly', True)]})
    lot_id = fields.Many2one(
        'stock.production.lot', 'Lot/Serial No.',
        domain="[('product_id', '=', product_id), ('company_id', '=', company_id)]", check_company=True)
    tracking = fields.Selection(string='Product Tracking', readonly=True, related="product_id.tracking")
    product_qty = fields.Float(
        'Quantity', default=1.0,
        digits='Product Unit of Measure', required=True)
    product_uom_id = fields.Many2one(
        'uom.uom', 'UoM',
        required=True,
        domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')
    bom_line_id = fields.Many2one('mrp.bom.line', 'BoM Line', check_company=True)
    company_id = fields.Many2one(
        related='dismantle_process_id.company_id', store=True, index=True, readonly=True)
    user_id = fields.Many2one(
        related='dismantle_process_id.user_id', store=True, index=True, readonly=True)
    state = fields.Selection(
        related='dismantle_process_id.state', string='Dismantle Status', copy=False, store=True)
    destination_location = fields.Many2one(
        'stock.location', 'Destination Location',
        domain="[('usage','=','internal'), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        check_company=True,
        related='dismantle_process_id.dismantle_location', readonly=False,
        help="Location where you want to send the components resulting from the dismantle order.")
    scrap = fields.Boolean(string='Scrap', default=False)
    scrap_location_id = fields.Many2one('stock.location', "Scrap Location", check_company=True, readonly=True,
                                        states={'draft': [('readonly', False)], 'transferred': [('readonly', False)]},
                                        domain="[('scrap_location','=',True), '|', ('company_id', '=', company_id), ('company_id', '=', False)]")

    @api.onchange('scrap')
    def load_scrap_location(self):
        for record in self:
            if record.scrap:
                record.scrap_location_id = self.env['stock.location'].search([('scrap_location', '=', True), '|',
                                                                              ('company_id', '=', record.company_id.id),
                                                                              ('company_id', '=', False)], limit=1).id

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.product_uom_id = self.product_id.uom_id.id


class StockMove(models.Model):
    _inherit = 'stock.move'

    produce_dismantle_id = fields.Many2one('dismantle.process', 'Produced Dismantle Order', check_company=True)
    consume_dismantle_id = fields.Many2one('dismantle.process', 'Consumed Dismantle Order', check_company=True)
    dismantle_product_line_id = fields.Many2one('dismantle.product.line', 'Dismantle Product Line', check_company=True)


class StockScrap(models.Model):
    _inherit = 'stock.scrap'

    sales_return_qc_id = fields.Many2one('dismantle.process', string="Sales Return QC", copy=False)
    dismantle_process_id = fields.Many2one('dismantle.process', string="Dismantled Scrap", copy=False)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    sales_return_qc_dismantle_id = fields.Many2one("dismantle.process", string="Sales Return Dismantle Transfer", copy=False)
    sales_return_qc_repair_id = fields.Many2one("dismantle.process", string="Sales Return Repair Transfer", copy=False)
    sales_return_qc_repair_delivery_id = fields.Many2one("dismantle.process", string="Sales Return Repaired Delivery", copy=False)

