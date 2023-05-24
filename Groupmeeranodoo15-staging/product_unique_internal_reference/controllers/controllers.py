# -*- coding: utf-8 -*-
# from odoo import http


# class ProductUniqueInternalReference(http.Controller):
#     @http.route('/product_unique_internal_reference/product_unique_internal_reference', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/product_unique_internal_reference/product_unique_internal_reference/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('product_unique_internal_reference.listing', {
#             'root': '/product_unique_internal_reference/product_unique_internal_reference',
#             'objects': http.request.env['product_unique_internal_reference.product_unique_internal_reference'].search([]),
#         })

#     @http.route('/product_unique_internal_reference/product_unique_internal_reference/objects/<model("product_unique_internal_reference.product_unique_internal_reference"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('product_unique_internal_reference.object', {
#             'object': obj
#         })
