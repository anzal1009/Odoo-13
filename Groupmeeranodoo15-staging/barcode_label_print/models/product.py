# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models,_,api

class ProductBrand(models.Model):
    _inherit = 'product.product'

    dimensions = fields.Char(string='Dimensions')
    content = fields.Char(string='Content')
    suffix = fields.Char(string='Suffix',default="AB")
    serial_no = fields.Integer(string='Serial NO')
    # label_category = fields.Many2one('label.category',string='Label Category')
    product_mrp = fields.Float(string='MRP')

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    label_category = fields.Many2one('label.category',string='Label Category')
class productAttribute(models.Model):
    _inherit = 'product.attribute'

    label_print= fields.Boolean(string='Label Print')