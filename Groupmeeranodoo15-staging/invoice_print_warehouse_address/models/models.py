# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Accountmove(models.Model):
    _inherit = 'account.move'

    warehouse_id = fields.Many2one('stock.warehouse', string="Warehouse")


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()

        if self.warehouse_id:
            invoice_vals['warehouse_id'] = self.warehouse_id.id
        return invoice_vals