# -*- coding: utf-8 -*-
# from odoo import http


# class SalesReturn(http.Controller):
#     @http.route('/sales_return/sales_return', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sales_return/sales_return/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sales_return.listing', {
#             'root': '/sales_return/sales_return',
#             'objects': http.request.env['sales_return.sales_return'].search([]),
#         })

#     @http.route('/sales_return/sales_return/objects/<model("sales_return.sales_return"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sales_return.object', {
#             'object': obj
#         })
