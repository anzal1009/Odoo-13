from odoo import models, fields

class ShopRecord(models.Model):
        _name = "staff.staff"


        sname = fields.Char(string='Staff Name')
        staffid = fields.Char(string='Staff Id')
        phone = fields.Char(string='Mobile No')
        saddres = fields.Char(string='Address')
        designation = fields.Selection([('m','manager'),('d','driver'),('a','accountant'),('s','salesman')],string='Designation')
        name = fields.Char(string='Short Name')

