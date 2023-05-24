from odoo import models, fields

class StaffRecord(models.Model):
        _name = "driver.driver"
        name = fields.Char(string='Name', required=True)
        # middle_name = fields.Char(string='Middle Name')
        last_name = fields.Char(string='Last Name', required=True)
        photo = fields.Binary(string='Photo')
        student_age = fields.Integer(string='Age')
        student_dob = fields.Date(string="Date of Birth")
        student_gender = fields.Selection([('m', 'Male'), ('f', 'Female'), ('o', 'Other')], string='Gender')
        student_blood_group = fields.Selection(
            [('A+', 'A+ve'), ('B+', 'B+ve'), ('O+', 'O+ve'), ('AB+', 'AB+ve'), ('A-', 'A-ve'), ('B-', 'B-ve'), ('O-', 'O-ve'),
            ('AB-', 'AB-ve')],
        string='Blood Group')
        nationality = fields.Many2one('staff.staff', string='Nationality')
        note =fields.Char(string='note')
        # staff_id_line_ids=fields.One2many('many.line','staff_id',string='staff_id')
        # active = fields.Boolean('Active', default=True)


 # class manyline(models.Model):
 #        _name = "many.line"
 #        name = fields.Char(string='name')
 #        age = fields.Integer(string='age')
 #        staff_id= fields.Char('driver.driver',string='staffid')