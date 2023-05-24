# -*- coding: utf-8 -*-
# from odoo import http


# class SalesReturnDismantle(http.Controller):
#     @http.route('/sales_return_dismantle/sales_return_dismantle', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sales_return_dismantle/sales_return_dismantle/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sales_return_dismantle.listing', {
#             'root': '/sales_return_dismantle/sales_return_dismantle',
#             'objects': http.request.env['sales_return_dismantle.sales_return_dismantle'].search([]),
#         })

#     @http.route('/sales_return_dismantle/sales_return_dismantle/objects/<model("sales_return_dismantle.sales_return_dismantle"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sales_return_dismantle.object', {
#             'object': obj
#         })
