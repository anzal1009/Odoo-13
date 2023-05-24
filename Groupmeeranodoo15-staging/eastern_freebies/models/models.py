# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    freebie = fields.Boolean(
        'Freebie', compute='_compute_freebie',
        inverse='_set_freebie', store=True)

    @api.depends('product_variant_ids', 'product_variant_ids.freebie')
    def _compute_freebie(self):
        unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            template.freebie = template.product_variant_ids.freebie
        for template in (self - unique_variants):
            template.freebie = False

    def _set_freebie(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.freebie = template.freebie


class ProductProduct(models.Model):
    _inherit = "product.product"

    freebie = fields.Boolean('Freebie', default=False)
