# -*- coding: utf-8 -*-

from odoo import models, fields, api
from num2words import num2words


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def english_amt2words(self, amount, currency, change, precision):
        change_amt = (amount - int(amount)) * pow(10, precision)
        words = '{main_amt} {main_word}'.format(
            main_amt=num2words(int(amount)),
            main_word=currency,
        )
        change_amt = int(round(change_amt))
        # words = words.title()
        if change_amt > 0:
            words += ' and {change_amt} {change_word}'.format(
                change_amt=num2words(change_amt),
                change_word=change,
            )
        words = words.title()
        words = words.replace('And', 'and')
        words = words.replace(',', '')
        words = words + " Only"
        return words

    def cgst_sgst_grouped_tax(self):
        for record in self:
            grouped_tax = {}
            taxes = {}
            cgst_group = self.env.ref("l10n_in.cgst_group")
            sgst_group = self.env.ref("l10n_in.sgst_group")
            igst_group = self.env.ref("l10n_in.igst_group")
            for line in record.order_line.filtered(lambda x: x.taxes_id):
                vals = line._prepare_compute_all_values()
                tax_discount_policy = self.env["ir.config_parameter"].sudo().get_param(
                    "bi_sale_purchase_discount_with_tax.tax_discount_policy")
                # res_config = self.env['res.config.settings'].sudo().search([], order="id desc", limit=1)
                if tax_discount_policy:
                    if tax_discount_policy == 'untax':
                        if line.discount_type == 'line':
                            if line.discount_method == 'fix':
                                price = (vals['price_unit'] * vals['quantity']) - line.discount_amount
                                taxes = line.taxes_id.compute_all(price, vals['currency'], 1, vals['product'],
                                                                  vals['partner'])
                            elif line.discount_method == 'per':
                                price = (vals['price_unit'] * vals['quantity']) * (
                                            1 - (line.discount_amount or 0.0) / 100.0)
                                price_x = ((vals['price_unit'] * vals['quantity']) - (
                                            (vals['price_unit'] * vals['quantity']) * (
                                                1 - (line.discount_amount or 0.0) / 100.0)))
                                taxes = line.taxes_id.compute_all(price, vals['currency'], 1, vals['product'],
                                                                  vals['partner'])
                            else:
                                taxes = line.taxes_id.compute_all(**line._prepare_compute_all_values())
                        else:
                            taxes = line.taxes_id.compute_all(**line._prepare_compute_all_values())
                    elif tax_discount_policy == 'tax':
                        price_x = 0.0
                        if line.discount_type == 'line':
                            taxes = line.taxes_id.compute_all(**line._prepare_compute_all_values())
                        else:
                            taxes = line.taxes_id.compute_all(**line._prepare_compute_all_values())
                    else:
                        taxes = line.taxes_id.compute_all(**line._prepare_compute_all_values())
                else:
                    taxes = line.taxes_id.compute_all(**line._prepare_compute_all_values())

                for tax in taxes['taxes']:
                    if tax['id'] in grouped_tax:
                        grouped_tax[tax['id']]['amount'] += tax['amount']
                    else:
                        tax_obj = self.env['account.tax'].browse(tax['id'])
                        if tax_obj.tax_group_id.id == cgst_group.id:
                            tax_name = 'Input CGST @'
                        elif tax_obj.tax_group_id.id == sgst_group.id:
                            tax_name = 'Input SGST @'
                        elif tax_obj.tax_group_id.id == igst_group.id:
                            tax_name = 'Input IGST @'
                        else:
                            tax_name = tax['name']
                        grouped_tax[tax['id']] = {
                                        'name': tax_name,
                                        'rate': tax_obj.amount,
                                        'amount': tax['amount']
                                    }
            return grouped_tax
