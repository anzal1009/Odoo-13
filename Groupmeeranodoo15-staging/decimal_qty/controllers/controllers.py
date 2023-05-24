# -*- coding: utf-8 -*-
# from odoo import http


# class DecimalQty(http.Controller):
#     @http.route('/decimal_qty/decimal_qty', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/decimal_qty/decimal_qty/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('decimal_qty.listing', {
#             'root': '/decimal_qty/decimal_qty',
#             'objects': http.request.env['decimal_qty.decimal_qty'].search([]),
#         })

#     @http.route('/decimal_qty/decimal_qty/objects/<model("decimal_qty.decimal_qty"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('decimal_qty.object', {
#             'object': obj
#         })
