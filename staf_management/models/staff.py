from odoo import models, fields

class StaffRecord(models.Model):
        _name = "staff.staff"
        name = fields.Char(string='Name', required=True)
        middle_name = fields.Char(string='Middle Name')
        last_name = fields.Char(string='Last Name', required=True)
        student_age = fields.Integer(string='Age')
        student_gender = fields.Selection([('m', 'Male'), ('f', 'Female'), ('o', 'Other')], string='Gender')
        nationality = fields.Many2one('staff.staff', string='Nationality')
        # active = fields.Boolean('Active', default=True)

