from odoo import models, fields, _


class PlotRecord(models.Model):
    _name = "plot.customer"

    name = fields.Char(string='Customer Name')
    phone = fields.Char(string='Mobile No')
    addres = fields.Char(string='Address')
    gmail = fields.Char(string='Gmail id')
    photo = fields.Binary(string='Photo')
    name_count = fields.Integer(string='Name Count', compute='_compute_name_count')
    phone_count = fields.Integer(string='Phone Count', compute='_compute_phone_count')



    def _compute_name_count(self):
        name_count = self.env['plot.enquiry'].search_count([('name', '=', self.name)])
        self.name_count = name_count

    def action_open_enquiry(self):
        return {
            'name': _('Enquiry'),
            'domain': [('name', '=', self.id)],
            'res_model': 'plot.enquiry',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }

    def _compute_phone_count(self):
        phone_count = self.env['plot.enquiry'].search_count([('phone', '=', self.phone)])
        self.phone_count = phone_count

    def action_open_enquiry(self):
        return {
            'name': _('Enquiry'),
            'domain': [('phone', '=', self.phone)],
            'res_model': 'plot.enquiry',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }
