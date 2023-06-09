# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'


class ReportInvoiceWithHideQty(models.AbstractModel):
    _name = 'report.custom_credit_note_print.report_invoice_custom'
    _description = 'Account report with payment lines Hide Qty'
    _inherit = 'report.account.report_invoice'

    @api.model
    def _get_report_values(self, docids, data=None):
        rslt = super()._get_report_values(docids, data)
        rslt['report_type'] = data.get('report_type') if data else ''
        return rslt
