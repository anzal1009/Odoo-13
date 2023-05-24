import mysql.connector

import qrcode
import base64
from io import BytesIO

from odoo import api, models, fields, _


# class InheritSales(models.Model):
#     _inherit = "sale.order"
#
#     qr_code = fields.Char(string='qr')


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Patient Name', tracking=True)
    name_seq = fields.Char(string='Patient ID', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    age = fields.Char(string='Age', tracking=True)
    photo = fields.Binary(string='Photo')
    gender = fields.Selection([('m', 'Male'), ('f', 'Female'), ('o', 'Other'), ], string='Gender')
    qr_code = fields.Binary("QR Code", attachment=True, store=True)
    note = fields.Text(string='Description', tracking=True)
    appointment_count = fields.Integer(string='Appointment Count', compute='_compute_appointment_count')

    def _compute_appointment_count(self):
        appointment_count = self.env['hospital.appoinment'].search_count([('name', '=', self.id)])
        self.appointment_count = appointment_count

    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'New Patient'

        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.patient') or _('New')

        res = super(HospitalPatient, self).create(vals)
        return res

    def action_open_appoinments(self):
        return {
            'name': _('Appointments'),
            'domain': [('name', '=', self.id)],
            'res_model': 'hospital.appoinment',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }

    # inserting data from database

    def action_patient(self):
        vals = {
            'name': "raman",
            'age': "20",
        }

        action_patient = self.env['hospital.patient'].create(vals)
        # print("qwe")

    #
    # from odoo import models, fields, api
    # class ProductQR(models.Model):
    #     _inherit = "product.template"
    #     qr_code = fields.Binary("QR Code", attachment=True, store=True)
    #

    # @api.onchange('default_code')
    # def generate_qr_code(self):
    #     qr = qrcode.QRCode(
    #         version=1,
    #         error_correction=qrcode.constants.ERROR_CORRECT_L,
    #         box_size=10,
    #         border=4,
    #     )
    #     qr.add_data(self.default_code)
    #     qr.make(fit=True)
    #     img = qr.make_image()
    #     temp = BytesIO()
    #     img.save(temp, format="PNG")
    #     qr_image = base64.b64encode(temp.getvalue())
    #     self.qr_code = qr_image

    @api.onchange('name')
    def generate_qr_code(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.name)
        qr.make(fit=True)
        img = qr.make_image()
        temp = BytesIO()
        img.save(temp, format="PNG")
        qr_image = base64.b64encode(temp.getvalue())
        self.qr_code = qr_image

    def action_patient2(self):

        mydb = mysql.connector.connect(

            host="192.168.0.101",
            user="anzal",
            password="anzal",
            database="deepa"
        )
        mycursor = mydb.cursor()

        mycursor.execute("SELECT * FROM tbl_staff")

        myresult = mycursor.fetchall()

        for x in myresult:
            vals = {
                'name': x[3],
                'age': x[5]
            }
            action_patient2 = self.env['hospital.patient'].create(vals)
            print(action_patient2)



# testing...


    def action_get(self):
        vals = {
            'partner_id': "raman",

        }

        action_get = self.env['sale.order'].create(vals)