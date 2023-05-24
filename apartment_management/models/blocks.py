from odoo import models, fields

class ApartmentRecord(models.Model):
        _name = "apartment.blocks"


        # name = fields.Many2one('apartment.configuration',string='Project Name')
        # dist = fields.Char(string='District',related='name.dist')
        name = fields.Char(string='Block Name')
        dist = fields.Char(string='Block Id')