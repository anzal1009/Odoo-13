# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    service_seq = fields.Char('Service Sequence')

    @api.onchange('detailed_type')
    def assign_service_sequence(self):
        for record in self:
            if record.detailed_type == 'service' and not record.service_seq:
                self_comp = self.with_company(self.company_id)
                record.service_seq = self_comp.env['ir.sequence'].next_by_code('product.service.sequence')


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.onchange('detailed_type')
    def assign_service_sequence(self):
        for record in self:
            if record.detailed_type == 'service' and not record.service_seq:
                self_comp = self.with_company(self.company_id)
                record.service_seq = self_comp.env['ir.sequence'].next_by_code('product.service.sequence')
