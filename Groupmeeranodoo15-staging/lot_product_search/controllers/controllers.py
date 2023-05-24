# -*- coding: utf-8 -*-
# from odoo import http


# class LotProductSearch(http.Controller):
#     @http.route('/lot_product_search/lot_product_search', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/lot_product_search/lot_product_search/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('lot_product_search.listing', {
#             'root': '/lot_product_search/lot_product_search',
#             'objects': http.request.env['lot_product_search.lot_product_search'].search([]),
#         })

#     @http.route('/lot_product_search/lot_product_search/objects/<model("lot_product_search.lot_product_search"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('lot_product_search.object', {
#             'object': obj
#         })
