from odoo import api, models, fields


class CreateEnquiryWizard(models.TransientModel):
    _name = "create.enquiry.wizard"

    name = fields.Many2one('plot.customer', string='Customer Name')
    phone = fields.Char(string="Mobile no")
    location = fields.Selection([('k', 'kochi'), ('m', 'malappuram'), ('t', 'trivandrum'), ('a', 'alappuzha')],
                                string='Location')

    def action_create(self):
        vals = {
            'name': self.name.id,
            'phone': self.phone,
            'location':self.location,
        }

        new_appointment = self.env['plot.enquiry'].create(vals)
