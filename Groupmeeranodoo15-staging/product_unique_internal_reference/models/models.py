# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import ValidationError, UserError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # _sql_constraints = [
    #     ('uniq_defaut_code', 'unique(default_code)',
    #      "A external reference already exists with this name . External reference must be unique!"),
    # ]
    # default_code = fields.Char(required=1)

    @api.constrains('default_code')
    def _check_unique_code(self):
        for product in self:
            if product.default_code:
                product_reference = self.env['product.product'].search_count([('default_code', '=', product.default_code)])
                reference = self.env['product.template'].search_count([('default_code', '=', product.default_code)])
                if product_reference > 1 or reference > 1:
                    raise ValidationError(_('A Internal reference already exists with this name . Internal reference must be unique!'))


# class ProductProduct(models.Model):
#     _inherit = "product.product"
#
#     default_code = fields.Char(required=1)
