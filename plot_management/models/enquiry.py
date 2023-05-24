from odoo import models, fields,_


class PlotRecord(models.Model):
    _name = "plot.enquiry"

    name = fields.Many2one('plot.customer', string='Customer Name')
    phone = fields.Char(string='Mobile No')
    addres = fields.Char(string='Address')
    location = fields.Selection([('k', 'kochi'), ('m', 'malappuram'), ('t', 'trivandrum'), ('a', 'alappuzha')],
                                string='Location')
    location_count = fields.Integer(string='Location Count', compute='_compute_location_count')

    def _compute_location_count(self):
        location_count = self.env['plot.enquiry'].search_count([('location', '=', self.location)])
        self.location_count = location_count

    def action_open_enquiry(self):
            return {
                    'name': _('Enquiry'),
                    'domain': [('location', '=', self.location)],
                    'res_model': 'plot.enquiry',
                    'view_id': False,
                    'view_mode': 'tree,form',
                    'type': 'ir.actions.act_window',
            }

    def quality_check(self):
        print("clicked")

        # return {
        # }
