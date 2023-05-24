# -*- coding: utf-8 -*-
# from odoo import http


# class ProductCostMandatory(http.Controller):
#     @http.route('/product_cost_mandatory/product_cost_mandatory', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/product_cost_mandatory/product_cost_mandatory/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('product_cost_mandatory.listing', {
#             'root': '/product_cost_mandatory/product_cost_mandatory',
#             'objects': http.request.env['product_cost_mandatory.product_cost_mandatory'].search([]),
#         })

#     @http.route('/product_cost_mandatory/product_cost_mandatory/objects/<model("product_cost_mandatory.product_cost_mandatory"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('product_cost_mandatory.object', {
#             'object': obj
#         })
