# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    state = fields.Selection(selection_add=[('send_to_logistic_approval', 'Send to Approval'),
                                            ('stock_in_transit', 'Stock in Transit'),
                                            ('validate_confirm', 'Proceed To validate')])

    virtual_location = fields.Many2one('stock.location', string="Virtual Location", default=lambda self: self.env.company.internal_transfer_transit_location, domain="[('company_id', 'in', [id, False]), ('usage', '=', 'transit')]")
    tmp_source_location = fields.Many2one('stock.location', string="Temporary Source Location")

    tmp_destination_location = fields.Many2one('stock.location', string="Temporary Destination Location", default=lambda self: self.env['stock.picking.type'].browse(self._context.get('default_picking_type_id')).default_location_dest_id,)

    security_confirm = fields.Boolean("Security For Confirm", default=False, store=True)
    security_validate = fields.Boolean("Security For validate", compute='security_for_validate', store=True)

    @api.depends('picking_type_code', 'state', 'picking_type_id')
    def security_for_validate(self):
        for order in self:
            s = []
            if order.picking_type_code == 'internal':
                if order.state in ['draft', 'send_to_logistic_approval',
                                   'stock_in_transit', 'done', 'assigned']:
                    order.security_validate = True
            else:
                if order.state in ['draft', 'done']:
                    order.security_validate = True
                else:
                    order.security_validate = False

    def action_confirm(self):
        res = super(StockPicking, self).action_confirm()
        for order in self:
            if order.picking_type_code == 'internal':
                order.security_confirm = True
            else:
                order.security_confirm = False
        return res

    @api.model
    def create(self, vals):
        res = super(StockPicking, self).create(vals)
        for order in res:
            if order.picking_type_code == 'internal':
                if order.show_mark_as_todo == True:
                    order.security_confirm = False
                else:
                    order.security_confirm = True

            else:
                order.security_confirm = False
                order.security_validate = False
        return res

    def confirm_button(self):
        for order in self:
            if order.location_id not in self.env.user.allowed_location_ids:
                raise UserError(_("You are not allowed to confirm this transfer. Please contact administrator"))
            order.write({'state': 'send_to_logistic_approval',
                         'tmp_destination_location': order.location_dest_id.id})

    def stock_transfer(self):
        if self.location_dest_id not in self.env.user.allowed_location_ids:
            raise UserError(_("You are not allowed to confirm this transfer. Please contact administrator"))

        for i in self.move_line_ids:
            i.location_dest_id = self.virtual_location.id
        self.ensure_one()
        ctx = dict(self.env.context)
        ctx.pop('default_immediate_transfer', None)
        self = self.with_context(ctx)
        pickings_without_moves = self.browse()
        pickings_without_quantities = self.browse()
        pickings_without_lots = self.browse()
        products_without_lots = self.env['product.product']
        for picking in self:
            if not picking.move_lines and not picking.move_line_ids:
                pickings_without_moves |= picking

            picking.message_subscribe([self.env.user.partner_id.id])
            picking_type = picking.picking_type_id
            precision_digits = self.env['decimal.precision'].precision_get('Product Unit of Measure')
            no_quantities_done = all(
                float_is_zero(move_line.qty_done, precision_digits=precision_digits) for move_line in
                picking.move_line_ids.filtered(lambda m: m.state not in ('done', 'cancel')))
            no_reserved_quantities = all(
                float_is_zero(move_line.product_qty, precision_rounding=move_line.product_uom_id.rounding) for move_line
                in picking.move_line_ids)
            if no_reserved_quantities and no_quantities_done:
                pickings_without_quantities |= picking

            if picking_type.use_create_lots or picking_type.use_existing_lots:
                lines_to_check = picking.move_line_ids
                if not no_quantities_done:
                    lines_to_check = lines_to_check.filtered(
                        lambda line: float_compare(line.qty_done, 0, precision_rounding=line.product_uom_id.rounding))
                for line in lines_to_check:
                    product = line.product_id
                    if product and product.tracking != 'none':
                        if not line.lot_name and not line.lot_id:
                            pickings_without_lots |= picking
                            products_without_lots |= product

        if not self._should_show_transfers():
            if pickings_without_moves:
                raise UserError(_('Please add some items to move.'))
            if pickings_without_quantities:
                raise UserError(self._get_without_quantities_error_message())
            if pickings_without_lots:
                raise UserError(_('You need to supply a Lot/Serial number for products %s.') % ', '.join(
                    products_without_lots.mapped('display_name')))
        else:
            message = ""
            if pickings_without_moves:
                message += _('Transfers %s: Please add some items to move.') % ', '.join(
                    pickings_without_moves.mapped('name'))
            if pickings_without_quantities:
                message += _(
                    '\n\nTransfers %s: You cannot validate these transfers if no quantities are reserved nor done. To force these transfers, switch in edit more and encode the done quantities.') % ', '.join(
                    pickings_without_quantities.mapped('name'))
            if pickings_without_lots:
                message += _('\n\nTransfers %s: You need to supply a Lot/Serial number for products %s.') % (
                ', '.join(pickings_without_lots.mapped('name')),
                ', '.join(products_without_lots.mapped('display_name')))
            if message:
                raise UserError(message.lstrip())
        # Run the pre-validation wizards. Processing a pre-validation wizard should work on the
        # moves and/or the context and never call `_action_done`.
        if not self.env.context.get('button_validate_picking_ids'):
            self = self.with_context(button_validate_picking_ids=self.ids)
        res = self._pre_action_done_hook()
        if res is not True:
            return res

        todo_moves = self.mapped('move_lines').filtered(
            lambda self: self.state in ['draft', 'waiting', 'partially_available', 'assigned', 'confirmed'])
        # Check if there are ops not linked to moves yet
        for pick in self:
            if pick.owner_id:
                pick.move_lines.write({'restrict_partner_id': pick.owner_id.id})
                pick.move_line_ids.write({'owner_id': pick.owner_id.id})
            for ops in pick.move_line_ids.filtered(lambda x: not x.move_id):
                # Search move with this product
                moves = pick.move_lines.filtered(lambda x: x.product_id == ops.product_id)
                moves = sorted(moves, key=lambda m: m.quantity_done < m.product_qty, reverse=True)
                if moves:
                    ops.move_id = moves[0].id
                else:
                    new_move = self.env['stock.move'].create({
                        'name': _('New Move:') + ops.product_id.display_name,
                        'product_id': ops.product_id.id,
                        'product_uom_qty': ops.qty_done,
                        'product_uom': ops.product_uom_id.id,
                        'description_picking': ops.description_picking,
                        'location_id': pick.location_id.id,
                        'location_dest_id': pick.virtual_location.id,
                        'picking_id': pick.id,
                        'picking_type_id': pick.picking_type_id.id,
                        'restrict_partner_id': pick.owner_id.id,
                        'company_id': pick.company_id.id,
                    })
                    ops.move_id = new_move.id
                    new_move._action_confirm()
                    todo_moves |= new_move
            todo_moves._action_done(cancel_backorder=self.env.context.get('cancel_backorder'))
            todo_moves.write({'state': 'assigned', 'date': fields.Datetime.now()})
            # self.write({'date_done': fields.Datetime.now()})
            self._send_confirmation_email()
            self.state = 'stock_in_transit'

    def confirm_validation(self):
        if self.location_id not in self.env.user.allowed_location_ids:
            raise UserError(_("You are not allowed to confirm this transfer. Please contact administrator"))

        if self.location_dest_id:
            for i in self.move_line_ids:
                i.location_id = self.virtual_location.id
                i.location_dest_id = self.location_dest_id.id

        for order in self:
            order.write({
                'tmp_source_location': order.location_id,
                # 'location_id': order.virtual_location,
                'state': 'validate_confirm'
            })
