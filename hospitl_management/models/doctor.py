from odoo import models, fields

class HospitalPatient(models.Model):
        _name = "hospital.doctor"


        name = fields.Char(string='Doctor Name')
        staffid = fields.Char(string='Doc Id')
        phone = fields.Char(string='Mobile No')
        # appointment_count = fields.Integer(string='Appointment Count', compute='_compute_appointment_count')
        #
        # def _compute_appointment_count(self):
        #         appointment_count = self.env['hospital.appoinment'].search_count([('name', '=', self.id)])
        #         self.appointment_count = appointment_count





