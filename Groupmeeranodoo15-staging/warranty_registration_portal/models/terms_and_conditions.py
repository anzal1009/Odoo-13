# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from ast import literal_eval
from odoo.exceptions import AccessError, UserError, ValidationError




class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    terms_and_conditions = fields.Html(string="Terms and Conditions")


    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        res['terms_and_conditions'] = (get_param('warranty_registration_portal.terms_and_conditions'))
        return res



    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('warranty_registration_portal.terms_and_conditions', self.terms_and_conditions)
        return res

    # self.env["ir.config_parameter"].sudo().get_param(
    #     "warranty_registration_portal.terms_and_conditions")