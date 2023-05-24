# -*- coding: utf-8 -*-

from odoo import models, fields, tools, api, _
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    standard_price = fields.Float(
        'Cost', compute='_compute_standard_price',
        inverse='_set_standard_price', search='_search_standard_price',
        digits='Product Price', groups="base.group_user",
        help="""In Standard Price & AVCO: value of the product (automatically computed in AVCO).
            In FIFO: value of the next unit that will leave the stock (automatically computed).
            Used to value the product when the purchase cost is not known (e.g. inventory adjustment).
            Used to compute margins on sale orders.""", required=1)

    # @api.depends_context('company')
    # @api.depends('product_variant_ids', 'product_variant_ids.standard_price')
    # def _compute_standard_price(self):
    #     # Depends on force_company context because standard_price is company_dependent
    #     # on the product_product
    #     unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
    #     for template in unique_variants:
    #         template.standard_price = template.product_variant_ids.standard_price
    #     for template in (self - unique_variants):
    #         template.standard_price = False


class ProductProduct(models.Model):
    _inherit = "product.product"

    standard_price = fields.Float(
        'Cost', company_dependent=True,
        digits='Product Price',
        groups="base.group_user",
        help="""In Standard Price & AVCO: value of the product (automatically computed in AVCO).
            In FIFO: value of the next unit that will leave the stock (automatically computed).
            Used to value the product when the purchase cost is not known (e.g. inventory adjustment).
            Used to compute margins on sale orders.""", required=1)

    # _sql_constraints = [
    #     ('check_standard_price', 'CHECK(detailed_type != "service" AND standard_price > 0)', 'Cost price should be positive.')
    # ]

    # @api.constrains('standard_price', 'detailed_type')
    # def _check_standard_price(self):
    #     for record in self:
    #         if record.detailed_type != 'service' and record.standard_price <= 0:
    #             raise ValidationError(
    #                 _('Cost of product must be greater than 0.0.'))

