# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    je_negative_balance_cash_bank = fields.Boolean(string='Enable -ve Balance checking in JE(Cash and Bank)', default=True)

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        je_negative_balance_cash_bank = ICPSudo.get_param('restrict_negative_cash_bank.je_negative_balance_cash_bank')
        res.update(je_negative_balance_cash_bank=je_negative_balance_cash_bank)
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        for rec in self:
            ICPSudo = rec.env['ir.config_parameter'].sudo()
            ICPSudo.set_param('restrict_negative_cash_bank.je_negative_balance_cash_bank', rec.je_negative_balance_cash_bank)


class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_post(self):
        je_negative_balance_cash_bank = self.env["ir.config_parameter"].sudo().get_param(
            "restrict_negative_cash_bank.je_negative_balance_cash_bank")
        if self.line_ids and je_negative_balance_cash_bank:
            bank_and_cash = self.env.ref('account.data_account_type_liquidity').id
            for line in self.line_ids.filtered(
                    lambda line: line.account_id.user_type_id.id == bank_and_cash):
                if (line.balance + line.account_id.current_balance) < 0:
                    raise ValidationError(_('Not able to post this JE due to -ve balance in %s.', line.account_id.name))
        return super(AccountMove, self).action_post()

    def _post(self, soft=True):
        je_negative_balance_cash_bank = self.env["ir.config_parameter"].sudo().get_param(
            "restrict_negative_cash_bank.je_negative_balance_cash_bank")
        if self.line_ids and je_negative_balance_cash_bank:
            bank_and_cash = self.env.ref('account.data_account_type_liquidity').id
            for line in self.line_ids.filtered(
                    lambda line: line.account_id.user_type_id.id == bank_and_cash):
                if (line.balance + line.account_id.current_balance) < 0:
                    raise ValidationError(_('Not able to post this JE due to -ve balance in %s.', line.account_id.name))
        return super(AccountMove, self)._post(soft=soft)
