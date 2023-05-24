# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseOrderType(models.Model):
    _name = 'purchase.order.type'
    _description = 'Purchase Order Type'

    name = fields.Char('PO Type', required=True)
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True,
                                 default=lambda self: self.env.company.id)

    sequence_id = fields.Many2one('ir.sequence', string='Sequence',
                                  domain="[('company_id', '=', company_id), ('code', '=', 'purchase.order')]", required=True)


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    po_type = fields.Many2one('purchase.order.type', string='PO Type')

    @api.model
    def create(self, vals):
        company_id = vals.get('company_id', self.default_get(['company_id'])['company_id'])
        self_comp = self.with_company(company_id)
        if 'po_type' in vals:
            po_type = self_comp.env['purchase.order.type'].browse(vals['po_type'])
            seq_date = None
            if 'date_order' in vals:
                seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.to_datetime(vals['date_order']))
            vals['name'] = po_type.sequence_id._next(sequence_date=seq_date) or '/'
        res = super(PurchaseOrder, self_comp).create(vals)
        return res
