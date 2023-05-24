from odoo import models, fields

class ApartmentRecord(models.Model):
        _name = "apartment.floors"


        # name = fields.Many2one('apartment.configuration',string='Project Name')
        dist = fields.Char(string='Floor Id')
        # block = fields.Many2one('apartment.blocks',string='Block Name')
        name = fields.Char( string='Floor')