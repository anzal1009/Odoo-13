# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    mrp_indent_ids = fields.One2many('mrp.indent', 'origin', 'MRP Indent')
    mrp_indent_count = fields.Integer(compute='_compute_mrp_indent_count', string='Store Request Count')
    indent_state = fields.Selection(
        [('draft', 'Not indented'),
         ('indent_created', 'Indent Created'),
         ('issued', 'Issued'),
         ('done', 'Done'),
         ('cancel', 'Indent Canceled'),
         ('reject', 'Indent Rejected')], string='Indent Status', readonly=True, copy=False, default='draft')

    def action_confirm(self):
        for production in self:
            if production.mrp_production_backorder_count > 1:
                return super(MrpProduction, self).action_confirm()
            indent_count = self.env['mrp.indent'].search([('origin', '=', production.id), ('state', '!=', 'cancel')])
            if not indent_count:
                vals = {
                    'origin': production.id,
                    'company_id': production.company_id.id,
                    'dest_location_id': production.location_src_id.id,
                    'location_id': production.company_id.mrp_indent_source_location.id
                }
                indent_product_lines = []
                for move in production.move_raw_ids:
                    indent_product_lines.append((0, 0, {
                        'product_id': move.product_id.id,
                        'to_consume_qty': move.product_uom_qty,
                        'uom_id': move.product_uom.id
                    }))
                vals['product_lines'] = indent_product_lines
                indent_obj = self.env['mrp.indent'].create(vals)
                production.indent_state = 'indent_created'
            else:
                if production.indent_state == 'indent_created':
                    raise UserError(_("Indent already created, Please wait for the store team approval"))
                elif production.indent_state == 'issued':
                    raise UserError(_("Indent has been approved by the store team. Please confirm the indent."))
                elif production.indent_state == 'done':
                    return super(MrpProduction, self).action_confirm()
                else:
                    raise UserError(_("Something went wrong. Please cancel this MO"))

    def mrp_indent_confirm(self):
        for order in self:
            indent_id = self.env['mrp.indent'].search([('origin', '=', order.id), ('state', '=', 'issued')])
            if indent_id:
                for indent in indent_id:
                    indent.action_receive_product()

    def action_cancel(self):
        indent_ids = self.env['mrp.indent'].search([('origin', '=', self.id)])
        if self.state == 'draft':
            if indent_ids:
                for indent in indent_ids:
                    indent.write({'state': 'cancel'})
            self.indent_state = 'cancel'
        return super(MrpProduction, self).action_cancel()

    def _compute_mrp_indent_count(self):
        for order in self:
            indent_count = self.env['mrp.indent'].search([('origin', '=', order.id)])
            order.mrp_indent_count = len(indent_count)
