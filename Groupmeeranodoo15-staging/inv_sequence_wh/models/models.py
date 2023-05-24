# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    warehouse_id = fields.Many2one('stock.warehouse', string="Warehouse", domain="[('company_id','=',company_id)]",
                                   readonly=True, states={'draft': [('readonly', False)]})

    @api.depends('posted_before', 'state', 'journal_id', 'date')
    def _compute_name(self):
        for move in self:
            if move.move_type in ('out_invoice', 'out_refund', 'in_refund'):
                if move.id and not move.warehouse_id:
                    raise UserError(_("Please select warehouse"))
                if not move.name or move.name == '/':
                    if move.move_type == 'out_invoice':
                        if move.id and not move.warehouse_id.sequence_id:
                            raise UserError(_("Please assign sequence to %s", move.warehouse_id.name))
                        move.name = move.warehouse_id.sequence_id._next() if move.warehouse_id else '/'
                    if move.move_type == 'out_refund':
                        if move.id and not move.warehouse_id.credit_note_sequence_id:
                            raise UserError(_("Please assign sequence to %s", move.warehouse_id.name))
                        move.name = move.warehouse_id.credit_note_sequence_id._next() if move.warehouse_id else '/'
                    if move.move_type == 'in_refund':
                        if move.id and not move.warehouse_id.debit_note_sequence_id:
                            raise UserError(_("Please assign sequence to %s", move.warehouse_id.name))
                        move.name = move.warehouse_id.debit_note_sequence_id._next() if move.warehouse_id else '/'
            else:
              return super(AccountMove, self)._compute_name()


class Warehouse(models.Model):
    _inherit = 'stock.warehouse'

    sequence_id = fields.Many2one('ir.sequence', string="Sequence for Invoice",
                                  domain="[('company_id','=',company_id)]")
    credit_note_sequence_id = fields.Many2one('ir.sequence', string="Sequence for Credit Note",
                                              domain="[('company_id','=',company_id)]")
    debit_note_sequence_id = fields.Many2one('ir.sequence', string="Sequence for Debit Note",
                                             domain="[('company_id','=',company_id)]")


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()

        if self.warehouse_id:
            invoice_vals['warehouse_id'] = self.warehouse_id.id
        return invoice_vals


class AccountMoveReversal(models.TransientModel):
    _inherit = 'account.move.reversal'

    warehouse_id = fields.Many2one('stock.warehouse', string="Warehouse", domain="[('company_id','=',company_id)]")

    def _prepare_default_reversal(self, move):
        res = super(AccountMoveReversal, self)._prepare_default_reversal(move)

        res.update({
            'warehouse_id': self.warehouse_id.id,
        })
        return res


class StockLocation(models.Model):
    _inherit = 'stock.location'

    sti_sequence_id = fields.Many2one('ir.sequence', string="Sequence for Delivery Challan/ STI",
                                             domain="[('company_id','=',company_id)]")


class Picking(models.Model):
    _inherit = "stock.picking"

    @api.model
    def create(self, vals):
        defaults = self.default_get(['name', 'location_id', 'picking_type_id'])
        picking_type = self.env['stock.picking.type'].browse(
            vals.get('picking_type_id', defaults.get('picking_type_id')))
        if picking_type.code == 'internal':
            source_location = self.env['stock.location'].browse(
                vals.get('location_id', defaults.get('location_id')))
            if vals.get('name', '/') == '/' and defaults.get('name', '/') == '/' and vals.get('location_id',
                                                                                              defaults.get(
                                                                                                      'location_id')):
                if source_location.sti_sequence_id:
                    vals['name'] = source_location.sti_sequence_id.next_by_id()
        res = super(Picking, self).create(vals)
        return res
