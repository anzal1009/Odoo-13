from odoo import api, models, fields


class CreateAppointmentWizard(models.TransientModel):
    _name = "create.appoinment.wizard"

    name = fields.Many2one('hospital.patient', string='Patient Name', tracking=True,required=True)
    dname = fields.Many2one('hospital.doctor',string='Doctor Name',tracking=True,required=True)
    ap_date = fields.Date(string='Appoinmtment date')


    # def action_create(self):
    #     print("test")

    def action_create(self):
        vals = {
            'name': self.name.id,
            'dname': self.dname.id,
            'ap_date':self.ap_date,
        }

        new_appointment = self.env['hospital.appoinment'].create(vals)
