# -*- coding: utf-8 -*-

from odoo import models, fields, api
# name_search_keyword = []


class ProductProduct(models.Model):
    _inherit = 'product.product'

    stock_production_lot_ids = fields.One2many(
        comodel_name="stock.production.lot",
        inverse_name="product_id",
        string="Lot/Serial Numbers"
    )

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        if not args:
            args = []
        if name:
            positive_operators = ['=', 'ilike', '=ilike', 'like', '=like']
            product_ids = []
            if operator in positive_operators:
                product_ids = list(self._search([('stock_production_lot_ids.name', '=', name)] + args, limit=limit, access_rights_uid=name_get_uid))
                # name_search_keyword =[]
                # name_search_keyword.append(name)
                if not product_ids:
                    return super(ProductProduct, self)._name_search(name,args,operator,limit,name_get_uid)
            else:
                return super(ProductProduct, self)._name_search(name, args, operator, limit, name_get_uid)
        else:
            product_ids = self._search(args, limit=limit, access_rights_uid=name_get_uid)
        return product_ids

    # @api.model
    # def get_name_search_keyword(self):
    #     if name_search_keyword:
    #         return name_search_keyword[0]


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    stock_production_lot_ids = fields.One2many(
        comodel_name="stock.production.lot",
        compute="_compute_production_lot_ids",
        inverse="_set_production_lot_ids",
        string="Lot/Serial Numbers"
    )

    @api.depends('product_variant_ids', 'product_variant_ids.stock_production_lot_ids')
    def _compute_production_lot_ids(self):
        for p in self:
            if len(p.product_variant_ids) == 1:
                p.stock_production_lot_ids = p.product_variant_ids.stock_production_lot_ids

    def _set_production_lot_ids(self):
        for p in self:
            if len(p.product_variant_ids) == 1:
                p.product_variant_ids.stock_production_lot_ids = p.stock_production_lot_ids

    def _re_write_production_lot(self, vals):
        production_lot_vals = vals.get('stock_production_lot_ids')
        if production_lot_vals:
            for template in self:
                if len(template.product_variant_ids) == 1:
                    template.product_variant_ids.write({
                        'stock_production_lot_ids': production_lot_vals
                    })

    @api.model
    def create(self, vals):
        templates = super(ProductTemplate, self).create(vals)
        templates._re_write_production_lot(vals)
        return templates


# class StockMoveLine(models.Model):
#     _inherit = "stock.move.line"
#
#     @api.onchange('product_id')
#     def _onchange_product_id_select_lot(self):
#         if self.product_id:
#             name_search_keyword = self.product_id.get_name_search_keyword()
#             self.lot_id = self.env['stock.production.lot'].search([
#                 ('name', '=', name_search_keyword), ('product_id', '=', self.product_id.id)]).id



