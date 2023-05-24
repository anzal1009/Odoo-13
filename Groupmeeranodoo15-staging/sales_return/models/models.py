# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SalesReturn(models.Model):
    _name = 'sales.return'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Sales Return'
    _order = 'id desc'

    name = fields.Char('Seuence No.', required=True, index=True, copy=False, default='New')
    ref = fields.Char('Reference', copy=False,
                         help="Reference of the document that generated this sales return"
                              "request (e.g. a sales order, invoice)")
    date = fields.Date(string='Date', required=True, index=True, readonly=True, states={'draft': [('readonly', False)]},
                       copy=False, tracking=True, default=fields.Date.context_today)
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('transferred', 'Transferred'),
        # ('scrap', 'Scrapped'),
        # ('repair', 'Repaired'),
        # ('dismantle', 'Dismantled'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', required=True, readonly=True, copy=False, tracking=True,
        default='draft')
    # process = fields.Selection(selection=[
    #     ('scrap', 'Scrap'),
    #     ('dismantle', 'Dismantle'),
    #     ('repair', 'Repair'),
    #     ('resell', 'Resell'),
    # ], string='Process', copy=False, default='repair')
    company_id = fields.Many2one(comodel_name='res.company', string='Company',
                                 store=True, readonly=True, default=lambda self: self.env.company.id)
    user_id = fields.Many2one('res.users', string='User', index=True, tracking=True, default=lambda self: self.env.user,
                              check_company=True)
    currency_id = fields.Many2one('res.currency', 'Currency', required=True, states={'draft': [('readonly', False)]},
                                  default=lambda self: self.env.company.currency_id.id)
    partner_id = fields.Many2one('res.partner', readonly=True, tracking=True, states={'draft': [('readonly', False)]},
                                 check_company=True, string='Partner', change_default=True, required=True)
    picking_type_id = fields.Many2one('stock.picking.type', 'Operation Type', required=True, readonly=True,
                                      states={'draft': [('readonly', False)]},
                                      domain="[('sales_return','=',True), ('company_id', '=', company_id)]")
    location_dest_id = fields.Many2one('stock.location', string='Destination Location', check_company=True,
                                       readonly=True, required=True, states={'draft': [('readonly', False)]},
                                       domain="[('usage','=','internal'), ('company_id', '=', company_id)]")
    # scrap_location = fields.Many2one('stock.location', string='Scrap Location', check_company=True, readonly=True,
    #                                  states={'draft': [('readonly', False)], 'transferred': [('readonly', False)]},
    #                                  domain="[('scrap_location','=',True), ('company_id', '=', company_id)]")
    # repair_location = fields.Many2one('stock.location', string='Repair Location', check_company=True, readonly=True,
    #                                   states={'draft': [('readonly', False)], 'transferred': [('readonly', False)]},
    #                                   domain="[('repair_location','=',True), ('company_id', '=', company_id)]")
    # dismantle_location = fields.Many2one('stock.location', string='Dismantle Location', check_company=True, readonly=True,
    #                                   states={'draft': [('readonly', False)], 'transferred': [('readonly', False)]},
    #                                   domain="[('dismantle_location','=',True), ('company_id', '=', company_id)]")
    location_id = fields.Many2one('stock.location', "Source Location",
                                  default=lambda self: self.env['stock.picking.type'].browse(
                                      self._context.get('default_picking_type_id')).default_location_src_id,
                                  check_company=True, readonly=True, required=True,
                                  states={'draft': [('readonly', False)]},
                                  domain="[('usage','=','customer'), '|', ('company_id', '=', company_id), ('company_id', '=', False)]")
    sale_return_reason = fields.Many2one('sale.return.reason', string='Return Reason', required=True)
    reference_invoice_ids = fields.Many2many('account.move', string='Invoice References', copy=False,
                                             domain="[('move_type', '=', 'out_invoice'), ('state', '=', 'posted'), ('company_id', '=', company_id)]")
    credit_note = fields.Many2one("account.move", string='Credit Note', copy=False)
    picking_id = fields.Many2one('stock.picking', string='Transfer', copy=False)
    picking_id_status = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting Another Operation'),
        ('confirmed', 'Waiting'),
        ('assigned', 'Ready'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', compute='_compute_picking_id_state', copy=False, readonly=True, store=True)
    # scrap_id = fields.Many2one('stock.scrap', string='Scrap', copy=False)
    return_line = fields.One2many('sales.return.line', 'sale_return_id', string='Return Lines',
                                 states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True,
                                 auto_join=True)
    tax_country_id = fields.Many2one(
        comodel_name='res.country',
        compute='_compute_tax_country_id',
        # Avoid access error on fiscal position when reading a sale order with company != user.company_ids
        compute_sudo=True,
        help="Technical field to filter the available taxes depending on the fiscal country")

    product_id = fields.Many2one('product.product', related='return_line.product_id', string='Product')

    @api.depends('picking_id.state')
    def _compute_picking_id_state(self):
        for record in self:
            if record.picking_id:
                record.picking_id_status = record.picking_id.state

    # def action_view_scrap(self):
    #     self.ensure_one()
    #     action = self.env["ir.actions.actions"]._for_xml_id("stock.action_stock_scrap")
    #     scraps = self.env['stock.scrap'].search([('sales_return_id', '=', self.id)])
    #     action['domain'] = [('id', 'in', scraps.ids)]
    #     action['context'] = dict(self._context, create=False)
    #     return action

    @api.onchange('picking_type_id')
    def set_dest_source_location_id(self):
        for record in self:
            if record.picking_type_id.default_location_src_id:
                record.location_id = record.picking_type_id.default_location_src_id.id
            if record.picking_type_id.default_location_dest_id:
                record.location_dest_id = record.picking_type_id.default_location_dest_id.id

    @api.depends('company_id.account_fiscal_country_id')
    def _compute_tax_country_id(self):
        for record in self:
            record.tax_country_id = record.company_id.account_fiscal_country_id

    # def scrap_product(self):
    #     for line in self.return_line:
    #         scrap = self.env['stock.scrap'].create({
    #             'product_id': line.product_id.id,
    #             'product_uom_id': line.product_uom.id,
    #             'scrap_qty': line.product_uom_qty,
    #             'lot_id': line.lot_id.id,
    #             'location_id': self.location_dest_id.id,
    #             'scrap_location_id': self.scrap_location.id,
    #             'company_id': line.company_id.id,
    #             'sales_return_id': self.id,
    #         })
    #         scrap.action_validate()
    #     self.write({
    #         'state': 'scrap',
    #     })

    def action_return_products(self):
        for record in self:
            stock_picking = self.env['stock.picking'].create({
                'move_lines': [],
                'picking_type_id': record.picking_type_id.id,
                'state': 'draft',
                'origin': _("Return from %s") % record.name,
                'location_id': record.location_id.id,
                'location_dest_id': record.location_dest_id.id,
                'sales_return_id': record.id,
                'partner_id': record.partner_id.id,
            })
            for line in record.return_line:
                if line.product_uom_qty:
                    stock_move_line = self.env['stock.move.line'].create(
                        {
                            'picking_id': stock_picking.id,
                            'company_id': line.company_id.id,
                            'product_id': line.product_id.id,
                            'product_uom_id': line.product_uom.id,
                            'product_uom_qty': line.product_uom_qty,
                            'qty_done': line.product_uom_qty,
                            'lot_id': line.lot_id.id,
                            'location_id': stock_picking.location_id.id,
                            'location_dest_id': stock_picking.location_dest_id.id,

                        })
                    # stock_move = self.env['stock.move'].create(
                    #     {
                    #         'product_id': line.product_id.id,
                    #         'product_uom_qty': line.product_uom_qty,
                    #         'product_uom': line.product_uom.id,
                    #         'picking_id': stock_picking.id,
                    #         'state': 'draft',
                    #         'date': fields.Datetime.now(),
                    #         'location_id': stock_picking.location_id.id,
                    #         'location_dest_id': stock_picking.location_dest_id.id,
                    #         'picking_type_id': stock_picking.picking_type_id.id,
                    #         'warehouse_id': stock_picking.picking_type_id.warehouse_id.id,
                    #         'procure_method': 'make_to_stock',
                    #         'name': line.product_id.with_context(lang=self.env.user.lang).partner_ref
                    #     }
                    # )
            stock_picking.action_confirm()
            stock_picking.action_assign()
            stock_picking.button_validate()
            if stock_picking:
                record.write({
                    'picking_id': stock_picking.id,
                    'state': 'transferred',
                })

    @api.model
    def create(self, vals):
        company_id = vals.get('company_id', self.default_get(['company_id'])['company_id'])
        # Ensures default picking type and currency are taken from the right company.
        self_comp = self.with_company(company_id)
        vals['name'] = self_comp.env['ir.sequence'].next_by_code('sales.return') or '/'
        res = super(SalesReturn, self_comp).create(vals)
        return res

    def action_view_credit_note(self):
        invoices = self.mapped('credit_note')
        action = self.env["ir.actions.actions"]._for_xml_id("account.action_move_out_invoice_type")
        if len(invoices) == 1:
            form_view = [(self.env.ref('account.view_move_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = invoices.id
        else:
            action = {'type': 'ir.actions.act_window_close'}

        context = {
            'default_move_type': 'out_refund',
        }
        action['context'] = context
        return action

    def action_view_picking(self):
        action = self.env["ir.actions.actions"]._for_xml_id("stock.action_picking_tree_all")

        if self.picking_id:
            form_view = [(self.env.ref('stock.view_picking_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = self.picking_id.id
        # Prepare the context.
        picking_id = self.picking_id.filtered(lambda l: l.picking_type_id.code == 'incoming')
        if picking_id:
            picking_id = picking_id[0]
        else:
            picking_id = self.picking_id[0]
        # action['context'] = dict(self._context, default_partner_id=self.partner_id.id,
        #                          default_picking_type_id=picking_id.picking_type_id.id, default_origin=self.name,
        #                          default_group_id=picking_id.group_id.id)
        return action

    @api.ondelete(at_uninstall=False)
    def _unlink_except_draft_or_cancel(self):
        for order in self:
            if order.state not in ('draft', 'cancel'):
                raise UserError(
                    _('You can not delete a transferred sales return or a confirmed sales return.'))

    def action_cancel(self):
        for record in self:
            record.state = 'cancel'

    # # Dismantle - Start
    # dismantle_operation_type = fields.Many2one('stock.picking.type', 'Dismantle Operation Type', readonly=True,
    #                                            states={'transferred': [('readonly', False)],
    #                                                    'draft': [('readonly', False)]},
    #                                            domain="[('code','=','internal'), ('company_id', '=', company_id), ('default_location_dest_id', '=', dismantle_location)]")
    # dismantle_picking_id = fields.Many2one('stock.picking', string='Dismantle Internal Transfer', copy=False)
    #
    # @api.onchange('dismantle_location')
    # def load_dismantle_operation_type(self):
    #     for record in self:
    #         if record.dismantle_location:
    #             record.dismantle_operation_type = self.env['stock.picking.type'].search([
    #                 ('code', '=', 'internal'),  ('company_id', '=', record.company_id.id),
    #                 ('default_location_dest_id', '=', record.dismantle_location.id)], limit=1).id
    #
    # def dismantle_product(self):
    #     for record in self:
    #         stock_picking = self.env['stock.picking'].create({
    #             # 'move_lines': [],
    #             'picking_type_id': record.dismantle_operation_type.id,
    #             'state': 'draft',
    #             'origin': _("Dismantle doc - %s") % record.name,
    #             'location_id': record.location_dest_id.id,
    #             'location_dest_id': record.dismantle_location.id,
    #             'sales_return_dismantle_id': record.id,
    #         })
    #         for line in record.return_line:
    #             if line.product_uom_qty:
    #                 stock_move_line = self.env['stock.move.line'].create(
    #                     {
    #                         'picking_id': stock_picking.id,
    #                         'company_id': line.company_id.id,
    #                         'product_id': line.product_id.id,
    #                         'product_uom_id': line.product_uom.id,
    #                         # 'product_uom_qty': line.product_uom_qty,
    #                         'qty_done': line.product_uom_qty,
    #                         'lot_id': line.lot_id.id,
    #                         'location_id': stock_picking.location_id.id,
    #                         'location_dest_id': stock_picking.location_dest_id.id,
    #
    #                     })
    #         # stock_picking.action_confirm()
    #         # stock_picking.action_assign()
    #         stock_picking.button_validate()
    #         if stock_picking:
    #
    #             record.write({
    #                 'state': 'dismantle',
    #                 'dismantle_picking_id': stock_picking.id
    #             })
    #
    # def action_view_dismantle_transfer(self):
    #     action = self.env["ir.actions.actions"]._for_xml_id("stock.action_picking_tree_all")
    #
    #     if self.dismantle_picking_id:
    #         form_view = [(self.env.ref('stock.view_picking_form').id, 'form')]
    #         if 'views' in action:
    #             action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
    #         else:
    #             action['views'] = form_view
    #         action['res_id'] = self.dismantle_picking_id.id
    #     # Prepare the context.
    #     picking_id = self.dismantle_picking_id.filtered(lambda l: l.picking_type_id.code == 'internal')
    #     if picking_id:
    #         picking_id = picking_id[0]
    #     else:
    #         picking_id = self.dismantle_picking_id[0]
    #     return action
    #
    # # Dismantle - End
    #
    # # Repair - Start
    # repair_components = fields.One2many('repair.components', 'sale_return_id', string='Repair Components',
    #                                     readonly=True, states={'transferred': [('readonly', False)]}, copy=False,
    #                                     auto_join=True)
    #
    # repair_operation_type = fields.Many2one('stock.picking.type', 'Repair Operation Type', readonly=True,
    #                                         states={'transferred': [('readonly', False)],
    #                                                 'draft': [('readonly', False)]},
    #                                         domain="[('code','=','internal'), ('company_id', '=', company_id), ('default_location_dest_id', '=', repair_location)]")
    # repair_picking_id = fields.Many2one('stock.picking', string='Repair Internal Transfer', copy=False)
    # repair_delivery_id = fields.Many2one('stock.picking', string='Repair Delivery', copy=False)
    #
    # def repair_product(self):
    #     for record in self:
    #         stock_picking = self.env['stock.picking'].create({
    #             # 'move_lines': [],
    #             'picking_type_id': record.repair_operation_type.id,
    #             'state': 'draft',
    #             'origin': _("Repair doc - %s") % record.name,
    #             'location_id': record.location_dest_id.id,
    #             'location_dest_id': record.repair_location.id,
    #             'sales_return_repair_id': record.id,
    #         })
    #         for line in record.return_line:
    #             if line.product_uom_qty:
    #                 stock_move_line = self.env['stock.move.line'].create(
    #                     {
    #                         'picking_id': stock_picking.id,
    #                         'company_id': line.company_id.id,
    #                         'product_id': line.product_id.id,
    #                         'product_uom_id': line.product_uom.id,
    #                         # 'product_uom_qty': line.product_uom_qty,
    #                         'qty_done': line.product_uom_qty,
    #                         'lot_id': line.lot_id.id,
    #                         'location_id': stock_picking.location_id.id,
    #                         'location_dest_id': stock_picking.location_dest_id.id,
    #
    #                     })
    #
    #         for line in record.repair_components:
    #             if line.product_uom_qty:
    #                 stock_move_line = self.env['stock.move.line'].create(
    #                     {
    #                         'picking_id': stock_picking.id,
    #                         'company_id': line.company_id.id,
    #                         'product_id': line.product_id.id,
    #                         'product_uom_id': line.product_uom.id,
    #                         # 'product_uom_qty': line.product_uom_qty,
    #                         'qty_done': line.product_uom_qty,
    #                         'lot_id': line.lot_id.id,
    #                         'location_id': stock_picking.location_id.id,
    #                         'location_dest_id': stock_picking.location_dest_id.id,
    #                     })
    #
    #         # stock_picking.action_confirm()
    #         # stock_picking.action_assign()
    #         stock_picking.button_validate()
    #         if stock_picking:
    #             record.write({
    #                 'state': 'repair',
    #                 'repair_picking_id': stock_picking.id
    #             })
    #
    # def action_view_repair(self):
    #     action = self.env["ir.actions.actions"]._for_xml_id("stock.action_picking_tree_all")
    #
    #     if self.repair_picking_id:
    #         form_view = [(self.env.ref('stock.view_picking_form').id, 'form')]
    #         if 'views' in action:
    #             action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
    #         else:
    #             action['views'] = form_view
    #         action['res_id'] = self.repair_picking_id.id
    #     # Prepare the context.
    #     picking_id = self.repair_picking_id.filtered(lambda l: l.picking_type_id.code == 'internal')
    #     if picking_id:
    #         picking_id = picking_id[0]
    #     else:
    #         picking_id = self.repair_picking_id[0]
    #     return action
    #
    # def action_view_delivery(self):
    #     action = self.env["ir.actions.actions"]._for_xml_id("stock.action_picking_tree_all")
    #
    #     if self.repair_delivery_id:
    #         form_view = [(self.env.ref('stock.view_picking_form').id, 'form')]
    #         if 'views' in action:
    #             action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
    #         else:
    #             action['views'] = form_view
    #         action['res_id'] = self.repair_delivery_id.id
    #     # Prepare the context.
    #     picking_id = self.repair_delivery_id.filtered(lambda l: l.picking_type_id.code == 'outgoing')
    #     if picking_id:
    #         picking_id = picking_id[0]
    #     else:
    #         picking_id = self.repair_delivery_id[0]
    #     return action
    # # Repair - End

    def action_confirm(self):
        for record in self:
            # if record.process == 'repair':
            #     stock_picking = self.env['stock.picking'].create({
            #         # 'move_lines': [],
            #         'picking_type_id': record.picking_type_id.return_picking_type_id.id,
            #         'state': 'draft',
            #         'origin': _("Delivery - %s") % record.name,
            #         'location_id': record.repair_location.id,
            #         'location_dest_id': record.location_id.id,
            #         'sales_return_delivery_id': record.id,
            #         'partner_id': record.partner_id.id,
            #     })
            #     for line in record.return_line:
            #         if line.product_uom_qty:
            #             stock_move_line = self.env['stock.move.line'].create(
            #                 {
            #                     'picking_id': stock_picking.id,
            #                     'company_id': line.company_id.id,
            #                     'product_id': line.product_id.id,
            #                     'product_uom_id': line.product_uom.id,
            #                     # 'product_uom_qty': line.product_uom_qty,
            #                     'qty_done': line.product_uom_qty,
            #                     'lot_id': line.lot_id.id,
            #                     'location_id': stock_picking.location_id.id,
            #                     'location_dest_id': stock_picking.location_dest_id.id,
            #                 })
            #     for line in record.repair_components:
            #         if line.product_uom_qty:
            #             stock_move_line = self.env['stock.move.line'].create(
            #                 {
            #                     'picking_id': stock_picking.id,
            #                     'company_id': line.company_id.id,
            #                     'product_id': line.product_id.id,
            #                     'product_uom_id': line.product_uom.id,
            #                     # 'product_uom_qty': line.product_uom_qty,
            #                     'qty_done': line.product_uom_qty,
            #                     'lot_id': line.lot_id.id,
            #                     'location_id': stock_picking.location_id.id,
            #                     'location_dest_id': stock_picking.location_dest_id.id,
            #                 })
            #     # stock_picking.action_confirm()
            #     # stock_picking.action_assign()
            #     stock_picking.button_validate()
            #     if stock_picking:
            #         record.write({'repair_delivery_id': stock_picking.id})
            account_move = self.env['account.move'].create({
                'state': 'draft',
                'partner_id': record.partner_id.id,
                'ref': _("Return from %s") % record.name,
                'move_type': 'out_refund',
                'sales_return_id': record.id
            })
            for line in record.return_line:
                if line.product_uom_qty:
                    account_move_line = self.env['account.move.line'].create({
                        'move_id': account_move.id,
                        'product_id': line.product_id.id,
                        'quantity': line.product_uom_qty,
                        'product_uom_id': line.product_uom.id,
                        'price_unit': line.price_unit,
                        'tax_ids': [(4, i) for i in line.tax_id.ids],
                        'name': line._get_computed_name(),
                        'account_id': account_move.journal_id.default_account_id.id
                    })
            if account_move:
                record.write({
                    'credit_note': account_move.id,
                    'state': 'done',
                })


class SalesReturnLine(models.Model):
    _name = 'sales.return.line'
    _description = 'Sales Return Line'
    _order = 'sale_return_id, id'
    _check_company_auto = True

    sale_return_id = fields.Many2one('sales.return', string='Return Reference', required=True, ondelete='cascade',
                                     index=True, copy=False)
    # discount = fields.Float(string='Discount (%)', digits='Discount', default=0.0)
    # name = fields.Text(string='Description')
    price_unit = fields.Float('Unit Price', required=True, digits='Product Price', default=0.0)

    # price_subtotal = fields.Monetary(compute='_compute_amount', string='Subtotal', store=True)
    # price_tax = fields.Float(compute='_compute_amount', string='Total Tax', store=True)
    # price_total = fields.Monetary(compute='_compute_amount', string='Total', store=True)
    tax_id = fields.Many2many('account.tax', string='Taxes', context={'active_test': False})
    company_id = fields.Many2one(related='sale_return_id.company_id', string='Company', store=True, index=True)
    product_id = fields.Many2one(
        'product.product', string='Product',
        domain="[('sale_ok', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        change_default=True, ondelete='restrict', check_company=True)  # Unrequired company
    product_uom_qty = fields.Float(string='Quantity', digits='Product Unit of Measure', required=True, default=1.0)
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure',
                                  domain="[('category_id', '=', product_uom_category_id)]", ondelete="restrict")
    user_id = fields.Many2one(related='sale_return_id.user_id', store=True, string='User')
    currency_id = fields.Many2one(related='sale_return_id.currency_id', depends=['sale_return_id.currency_id'], store=True,
                                  string='Currency')
    partner_id = fields.Many2one(related='sale_return_id.partner_id', store=True, string='Customer')
    state = fields.Selection(
        related='sale_return_id.state', string='Order Status', copy=False, store=True)
    lot_id = fields.Many2one(
        'stock.production.lot', 'Lot/Serial Number',
        domain="[('product_id', '=', product_id), ('company_id', '=', company_id)]", check_company=True)
    product_reference = fields.Char('Product Reference', )
    tracking = fields.Selection(string='Product Tracking', readonly=True, related="product_id.tracking")

    @api.onchange('product_id')
    def product_id_change(self):
        if not self.product_id:
            return
        vals = {}
        if not self.product_uom or (self.product_id.uom_id.id != self.product_uom.id):
            vals['product_uom'] = self.product_id.uom_id
            vals['product_uom_qty'] = self.product_uom_qty or 1.0
        self._compute_tax_id()
        vals['price_unit'] = self.product_id.list_price
        vals['product_reference'] = self.product_id.default_code
        self.update(vals)

    def _compute_tax_id(self):
        for line in self:
            line = line.with_company(line.company_id)
            taxes = line.product_id.taxes_id.filtered(lambda t: t.company_id == line.env.company)
            line.tax_id = [(4, i.id) for i in taxes]

    def _get_computed_name(self):
        self.ensure_one()

        if not self.product_id:
            return ''

        if self.partner_id.lang:
            product = self.product_id.with_context(lang=self.partner_id.lang)
        else:
            product = self.product_id

        values = []
        if product.partner_ref:
            values.append(product.partner_ref)
        if product.description_sale:
            values.append(product.description_sale)
        return '\n'.join(values)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    sales_return_id = fields.Many2one("sales.return", string="Sales Return", copy=False)
    # sales_return_dismantle_id = fields.Many2one("sales.return", string="Sales Return Dismantle Transfer", copy=False)
    # sales_return_repair_id = fields.Many2one("sales.return", string="Sales Return Repair Transfer", copy=False)
    # sales_return_delivery_id = fields.Many2one("sales.return", string="Sales Return Repaired Delivery", copy=False)


class AccountMove(models.Model):
    _inherit = "account.move"

    sales_return_id = fields.Many2one('sales.return', string="Sales Return", copy=False)











