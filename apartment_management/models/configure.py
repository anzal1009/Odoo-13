from odoo import models, fields

class ApartmentRecord(models.Model):
        _name = "apartment.configuration"


        name = fields.Char(string='Project Name')
        dist = fields.Char(string='District')
        pid = fields.Char(string='Project Id')
        states =fields.Char(string='State')
        country =fields.Many2one('res.country',string='Country')



