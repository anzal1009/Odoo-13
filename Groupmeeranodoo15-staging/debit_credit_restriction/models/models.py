# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError,AccessError


class AccountMove(models.Model):
    _inherit = 'account.move'


    def action_post(self):
        """To check the selected customers due amount is exceed than
        blocking stage"""
        pay_type = ['in_refund', 'out_refund']
        for rec in self:
            if rec.reversed_entry_id and rec.move_type in pay_type:
                if rec.amount_total >= rec.reversed_entry_id.amount_total:
                    raise UserError(_(
                            "Exceeds the Invoice amount"))
        return super(AccountMove, self).action_post()