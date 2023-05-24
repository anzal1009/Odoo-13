# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import AccessDenied


class ResPartner(models.Model):
    _inherit = 'res.partner'

    day_so_block = fields.Boolean('Day wise SO Blocking', help='Activate the SO blocking')


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        if self.partner_id.day_so_block:
            current_date = fields.Date.context_today(self)
            overdue = self.env['account.move'].search(
                [('partner_id', '=', self.partner_id.id), ('invoice_date_due', '<', current_date),
                 ('state', '=', 'posted'), ('payment_state', 'in', ('not_paid', 'partial')),
                 ('move_type', '=', 'out_invoice')])
            if overdue:
                raise AccessDenied(_('Overdue. Please make the payment before SO confirmation '))

        res = super(SaleOrder, self).action_confirm()
        return res

