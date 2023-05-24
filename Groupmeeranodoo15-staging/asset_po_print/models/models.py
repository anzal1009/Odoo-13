# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    asset_seq = fields.Char('Asset Sequence')
    is_asset_product = fields.Boolean('Is Asset', default=False)

    @api.onchange('property_account_expense_id')
    def assign_asset_sequence(self):
        for record in self:
            if record.property_account_expense_id:
                if record.property_account_expense_id.user_type_id == self.env.ref('account.data_account_type_fixed_assets') and record.property_account_expense_id.create_asset != 'no':
                    record.is_asset_product = True
                    if not record.asset_seq:
                        self_comp = self.with_company(self.company_id)
                        record.asset_seq = self_comp.env['ir.sequence'].next_by_code('product.asset.sequence')
                else:
                    record.is_asset_product = False
                    # raise UserError(_("Expense account must be a fixed asset CoA"))
            else:
                record.is_asset_product = False


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.onchange('property_account_expense_id')
    def assign_asset_sequence(self):
        for record in self:
            if record.property_account_expense_id:
                if record.property_account_expense_id.user_type_id == self.env.ref(
                        'account.data_account_type_fixed_assets') and record.property_account_expense_id.create_asset != 'no':
                    record.is_asset_product = True
                    if not record.asset_seq:
                        self_comp = self.with_company(self.company_id)
                        record.asset_seq = self_comp.env['ir.sequence'].next_by_code('product.asset.sequence')
                else:
                    record.is_asset_product = False
                    # raise UserError(_("Expense account must be a fixed asset CoA"))
            else:
                record.is_asset_product = False


