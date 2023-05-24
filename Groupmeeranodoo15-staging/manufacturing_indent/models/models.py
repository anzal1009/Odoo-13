# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.tools import float_round
from odoo.exceptions import UserError, ValidationError
import datetime


class MrpIndent(models.Model):
    _name = 'mrp.indent'
    _inherit = ['mail.thread']
    _order = 'id desc'
    _description = 'Manufacturing Indent'

    @api.model
    def create(self, vals):
        if not vals.get('name') or vals['name'] == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('mrp.indent') or _('New')
        return super(MrpIndent, self).create(vals)

    name = fields.Char(string='name', readonly=True, copy=False, default=lambda x: _('New'))
    indent_date = fields.Datetime(string='Indent Date', required=True, default=fields.Datetime.now, readonly=True,
                                  states={'draft': [('readonly', False)]})
    origin = fields.Many2one('mrp.production', string='Source Document', readonly=True, copy=False)
    issued_date = fields.Datetime(string='Issued Date', readonly=True)
    issued_by = fields.Many2one('res.users', string='Issued by', readonly=True)
    received_date = fields.Datetime(string='Received Date', readonly=True)
    received_by = fields.Many2one('res.users', string='Received by', readonly=True)
    # move_lines = fields.One2many('stock.move', 'mrp_indent_id', string='Moves', copy=False, readonly=True)
    product_lines = fields.One2many('mrp.indent.product.lines', 'indent_id', string='Product', copy=False)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id,
                                 readonly=True, states={'draft': [('readonly', False)]})
    location_id = fields.Many2one('stock.location', string='Source Location', readonly=True, required=True,
                                  domain="[('usage', '=', 'internal'), ('company_id', 'in', [company_id, False])]",
                                  states={'draft': [('readonly', False)]})
    dest_location_id = fields.Many2one('stock.location', string='Destination Location', readonly=True, required=True,
                                  domain="[('usage', '=', 'internal'), ('company_id', 'in', [company_id, False])]",
                                  states={'draft': [('readonly', False)]})

    state = fields.Selection(
        [('draft', 'Draft'),
         ('issued', 'Issued'),
         ('received', 'Received'),
         ('cancel', 'Cancel'),
         ('reject', 'Rejected')], string='State', readonly=True, default='draft', track_visibility='onchange')

    def action_approve(self):
        for record in self:
            # if any(product.product_qty < product.balance_requirements for product in record.product_lines):
            #     raise ValidationError(_('Issued quantity must be greater than required.'))
            moves = self.env['stock.move']
            for line in record.product_lines:
                location_dest_id = record.company_id.mrp_indent_transit_location
                warehouse = record.location_id.warehouse_id
                move = self.env['stock.move'].create(
                    {
                        'name': record.name,
                        'date': datetime.datetime.now(),
                        'product_id': line.product_id.id,
                        'product_uom_qty': line.product_qty,
                        'product_uom': line.uom_id.id,
                        'procure_method': 'make_to_stock',
                        'location_dest_id': location_dest_id.id,
                        'location_id': record.location_id.id,
                        'warehouse_id': warehouse.id,
                        'mrp_indent_id': record.id,
                        'mrp_indent_product_line_id': line.id,
                        'company_id': record.company_id.id,
                    }
                )
                moves += move
            moves._action_confirm()
            for move in moves:
                if move.has_tracking != 'none':
                    self.env['stock.move.line'].create(
                        {
                            'move_id': move.id,
                            'lot_id': move.mrp_indent_product_line_id.lot_id.id,
                            'qty_done': move.product_uom_qty,
                            'product_id': move.product_id.id,
                            'product_uom_id': move.product_uom_id.id,
                            'location_id': move.location_id.id,
                            'location_dest_id': move.location_dest_id.id,
                        })
                else:
                    move.quantity_done = float_round(move.product_uom_qty, precision_rounding=move.product_uom.rounding)
            moves._action_done()
            record.write({
                'state': 'issued',
                'issued_date': datetime.datetime.now(),
                'issued_by': self.env.user.id
            })
            record.origin.write({'indent_state': 'issued'})
        return True

    def action_receive_product(self):
        for record in self:
            moves = self.env['stock.move']
            for line in record.product_lines:
                location_dest_id = record.dest_location_id
                warehouse = record.dest_location_id.warehouse_id
                move = self.env['stock.move'].create(
                    {
                        'name': record.name,
                        'date': datetime.datetime.now(),
                        'product_id': line.product_id.id,
                        'product_uom_qty': line.product_qty,
                        'product_uom': line.uom_id.id,
                        'procure_method': 'make_to_stock',
                        'location_dest_id': location_dest_id.id,
                        'location_id': record.company_id.mrp_indent_transit_location.id,
                        'warehouse_id': warehouse.id,
                        'mrp_indent_id': record.id,
                        'mrp_indent_product_line_id': line.id,
                        'company_id': record.company_id.id,
                    }
                )
                moves += move
            moves._action_confirm()
            for move in moves:
                if move.has_tracking != 'none':
                    self.env['stock.move.line'].create(
                        {
                            'move_id': move.id,
                            'lot_id': move.mrp_indent_product_line_id.lot_id.id,
                            'qty_done': move.product_uom_qty,
                            'product_id': move.product_id.id,
                            'product_uom_id': move.product_uom_id.id,
                            'location_id': move.location_id.id,
                            'location_dest_id': move.location_dest_id.id,
                        })
                else:
                    move.quantity_done = float_round(move.product_uom_qty, precision_rounding=move.product_uom.rounding)
            moves._action_done()
            record.write({
                'state': 'received',
                'received_date': datetime.datetime.now(),
                'received_by': self.env.user.id
            })
            record.origin.write({'indent_state': 'done'})
        return True

    def action_cancel(self):
        for record in self:
            record.origin.write({'indent_state': 'draft'})
            record.write({
                'state': 'cancel',
                'origin': False
            })

    def unlink(self):
        for record in self:
            if record.state not in ('cancel', 'draft'):
                raise UserError(_("You can only delete draft or cancelled indent"))
            record.origin.write({'indent_state': 'draft'})
            return super(MrpIndent, record).unlink()


class MrpIndentProductLines(models.Model):
    _name = 'mrp.indent.product.lines'
    _order = 'indent_id, id'
    _description = 'Indent Product Lines'

    indent_id = fields.Many2one('mrp.indent', string='Indent', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', required=True, readonly=True,
                                 states={'draft': [('readonly', False)]})
    product_qty = fields.Float(string='Issued Quantity', digits='Product Unit of Measure', readonly=True, states={'draft': [('readonly', False)]})
    to_consume_qty = fields.Float(string='To Consume', digits='Product Unit of Measure', required=True, readonly=True,
                                  states={'draft': [('readonly', False)]})
    wip_stock = fields.Float(string='WIP Stock', digits='Product Unit of Measure',
                             compute='_compute_product_available_in_wip')
    balance_requirements = fields.Float(string='Balance Requirements', digits='Product Unit of Measure',
                                        compute='_compute_balance_requirement', store=True)
    available_qty = fields.Float('Available Quantity', digits='Product Unit of Measure', compute='_compute_product_available_qty')

    uom_id = fields.Many2one('uom.uom', string='Unit of Measure', required=True, readonly=True,
                                  states={'draft': [('readonly', False)]})
    tracking = fields.Selection(string='Product Tracking', readonly=True, related="product_id.tracking")
    lot_id = fields.Many2one(
        'stock.production.lot', 'Lot/Serial No.',
        domain="[('product_id', '=', product_id), ('company_id', '=', company_id)]", check_company=True)
    state = fields.Selection(
        [('draft', 'Draft'),
         ('issued', 'Issued'),
         ('received', 'Received'),
         ('cancel', 'Cancel'),
         ('reject', 'Rejected')], string='State', default='draft', related='indent_id.state')
    company_id = fields.Many2one(
        related='indent_id.company_id', store=True, index=True, readonly=True)
    issued_by = fields.Many2one(related='indent_id.issued_by', store=True, string='Issued by', readonly=True)

    @api.depends('product_id', 'company_id', 'indent_id.location_id')
    def _compute_product_available_qty(self):
        for record in self:
            product_list = self.env['stock.quant'].read_group([('product_id', '=', record.product_id.id),
                                                               ('company_id', '=', record.company_id.id),
                                                               ('location_id', '=', record.indent_id.location_id.id),
                                                               ('available_quantity', '>', 0)],
                                                              ['product_id', 'location_id', 'available_quantity'],
                                                              ['product_id', 'location_id'], lazy=False)
            available_qty = 0
            for item in product_list:
                available_qty += item['available_quantity']
            record.available_qty = available_qty

    @api.depends('product_id', 'company_id', 'indent_id.dest_location_id')
    def _compute_product_available_in_wip(self):
        for record in self:
            product_list = self.env['stock.quant'].read_group([('product_id', '=', record.product_id.id),
                                                               ('company_id', '=', record.company_id.id),
                                                               ('location_id', '=', record.indent_id.dest_location_id.id),
                                                               ('available_quantity', '>', 0)],
                                                              ['product_id', 'location_id', 'available_quantity'],
                                                              ['product_id', 'location_id'], lazy=False)
            available_qty = 0
            for item in product_list:
                available_qty += item['available_quantity']
            record.wip_stock = available_qty

    @api.depends('wip_stock', 'to_consume_qty')
    def _compute_balance_requirement(self):
        for record in self:
            record.balance_requirements = record.to_consume_qty - record.wip_stock if record.to_consume_qty > record.wip_stock else 0

    # @api.constrains('product_qty')
    # def _check_issued_qty(self):
    #     for record in self:
    #         if record.product_qty < record.balance_requirements:
    #             raise ValidationError(_('Issued quantity of %s must be greater than required.') % (record.product_id.name))


class StockMove(models.Model):
    _inherit = 'stock.move'

    mrp_indent_id = fields.Many2one('mrp_indent_id', 'Mrp Indent', check_company=True)
    mrp_indent_product_line_id = fields.Many2one('mrp.indent.product.lines', 'MRP Indent Product Line', check_company=True)
