from odoo import models, fields

class ApartmentRecord(models.Model):
        _name = "apartment.unit"


        # name = fields.Many2one('apartment.configuration',string='Project Name')
        dist = fields.Char(string='Unit Id')
        # block = fields.Many2one('apartment.blocks',string='Block Name')
        name = fields.Char( string='Unit Type')
        desc = fields.Text(string='Description')