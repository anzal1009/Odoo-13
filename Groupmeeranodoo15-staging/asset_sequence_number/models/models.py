# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountAssetAsset(models.Model):
    _inherit = 'account.asset'

    sequence = fields.Char(readonly=True,copy=False, default='New')

    def validate(self):
        res = super(AccountAssetAsset, self).validate()
        for asset in self:
            new_sequence = self.env['ir.sequence'].next_by_code('account.asset.sequence') or 'New'
            asset.sequence = new_sequence
        return res