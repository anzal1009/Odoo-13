from odoo import models, fields

class StudentRecord(models.Model):
        _name = "product.product"
        product_id=fields.Integer(string='Product_id',required=True)
        name = fields.Char(string='Name', required=True)
        price= fields.Integer(string='price',required=True)

