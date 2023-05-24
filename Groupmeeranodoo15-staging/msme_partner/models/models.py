# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Partner(models.Model):
    _inherit = 'res.partner'

    is_msme = fields.Boolean(string="Is MSME", default=False)

    @api.onchange('is_msme')
    def load_property_supplier_payment_term_id(self):
        for record in self:
            if record.is_msme:
                record.property_supplier_payment_term_id = self.env.company.msme_payment_term_id
