# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict

from odoo import _, models
from odoo.exceptions import UserError


class BarcodeProductLabel(models.AbstractModel):
    _name = 'report.barcode_label_print.barcode_label1_product_view'
    _description = 'Product Label'

    def _get_report_values(self, docids, data):
        if data.get('active_model') == 'product.labels':
            Product = self.env['product.labels']
        else:
            raise UserError(_('model not defined, Please contact your administrator.'))

        quantity_by_product = defaultdict(list)
        for p, q in data.get('quantity_by_product').items():
            product = Product.browse(int(p))
            quantity_by_product[product].append((product.product_id.barcode, q))
        data['quantity'] = quantity_by_product

        return data

class BarcodeProductLabel2(models.AbstractModel):
    _name = 'report.barcode_label_print.barcode_label2_product_view'
    _description = 'Product Label'

    def _get_report_values(self, docids, data):
        if data.get('active_model') == 'product.labels':
            Product = self.env['product.labels']
        else:
            raise UserError(_('model not defined, Please contact your administrator.'))

        quantity_by_product = defaultdict(list)
        for p, q in data.get('quantity_by_product').items():
            product = Product.browse(int(p))
            quantity_by_product[product].append((product.product_id.barcode, q))
        data['quantity'] = quantity_by_product

        return data

class BarcodeProductLabel3(models.AbstractModel):
    _name = 'report.barcode_label_print.barcode_label3_product_view'
    _description = 'Product Label'

    def _get_report_values(self, docids, data):
        if data.get('active_model') == 'product.labels':
            Product = self.env['product.labels']
        else:
            raise UserError(_('model not defined, Please contact your administrator.'))

        quantity_by_product = defaultdict(list)
        for p, q in data.get('quantity_by_product').items():
            product = Product.browse(int(p))
            quantity_by_product[product].append((product.product_id.barcode, q))
        data['quantity'] = quantity_by_product

        return data

class BarcodeProductLabel4(models.AbstractModel):
    _name = 'report.barcode_label_print.barcode_label4_product_view'
    _description = 'Product Label'

    def _get_report_values(self, docids, data):
        if data.get('active_model') == 'product.labels':
            Product = self.env['product.labels']
        else:
            raise UserError(_('model not defined, Please contact your administrator.'))

        quantity_by_product = defaultdict(list)
        for p, q in data.get('quantity_by_product').items():
            product = Product.browse(int(p))
            quantity_by_product[product].append((product.product_id.barcode, q))
        data['quantity'] = quantity_by_product

        return data
