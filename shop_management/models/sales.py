from odoo import models, fields

class ShopRecord(models.Model):
        _name = "sales.sales"


        customer = fields.Many2one('res.partner',string='Customer Name')
        number = fields.Char(string='Invoice Number')
        address = fields.Char(string='Address')
        idate = fields.Date(string='Invoice Date')
        sdate = fields.Date(string='Shipping Date')
        salesperson = fields.Many2one('staff.staff',string='Sales Person'
                                      )
        sales_line_ids = fields.One2many('sales.line','sales_id',string='Sales line')



class Salesline(models.Model):
        _name = "sales.line"

        sno = fields.Char(string='Sno')
        product = fields.Many2one('res.product.template',string='Product Name')
        qty = fields.Char(string='Quantity')
        sales_id = fields.Many2one('sales.sales',string='Sales')
