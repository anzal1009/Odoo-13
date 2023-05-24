from odoo import models, fields,_ ,api

class HospitalPatient(models.Model):
        _name = "hospital.appoinment"
        _inherit = ['mail.thread', 'mail.activity.mixin']

        name_seq = fields.Char(string='Appointment ID', required=True, copy=False, readonly=True,
                               default=lambda self: _('New'))
        name = fields.Many2one('hospital.patient', string='Patient Name',tracking=True,required=True)
        # appoinment_id = fields.Char(string='Appoinment Id',tracking=True)
        age = fields.Char(string='Age',related='name.age')
        # photo = fields.Binary(string='Photo',related='name.photo')
        gender = fields.Selection([('m','Male'),('f','Female'),('o','Other'),],string='Gender',related='name.gender')
        dname = fields.Many2one('hospital.doctor',string='Doctor Name',tracking=True,required=True)
        ap_date = fields.Date(string='Check In')

        state = fields.Selection([('draft', 'Draft'),('pending', 'Pending'),('cancelled', 'Cancelled'),('confirmed', 'Confirmed')], default='draft',string='Status',tracking=True)

        def action_draft(self):
                self.state = 'draft'


        def action_confirm(self):
                self.state = 'confirmed'


        def action_pending(self):
                self.state ='pending'

        def action_cancel(self):
                self.state = 'cancelled'

        @api.model
        def create(self, vals):
                # if not vals.get('note'):
                #         vals['note'] = 'New Patient'

                if vals.get('name_seq', _('New')) == _('New'):
                        vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.appoinment') or _('New')

                res = super(HospitalPatient, self).create(vals)
                return res





