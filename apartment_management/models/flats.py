from odoo import models, fields


class ApartmentRecord(models.Model):
    _name = "apartment.flats"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Unit Name', tracking=True)
    projname = fields.Many2one('apartment.configuration', string='Project Name', tracking=True)
    bloname = fields.Many2one('apartment.blocks', string='Block Name', tracking=True)
    floor = fields.Many2one('apartment.floors', string='Floor', tracking=True)
    utype = fields.Many2one('apartment.unit', string='Unit type', tracking=True)
    desc = fields.Text(string='Description')
    price = fields.Char(string='Price', tracking=True)
    misc = fields.Char(string='misc')
    dist = fields.Char(string='District',related='projname.dist')

    state = fields.Selection(
        [('un', 'Un sold'), ('bo', 'Booked'), ('so', 'Sold')],
        default='un', string='Status', tracking=True)

    def action_booked(self):
        self.state = 'bo'

    def action_sold(self):
        self.state = 'so'

