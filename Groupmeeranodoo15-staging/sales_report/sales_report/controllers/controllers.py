# -*- coding: utf-8 -*-
# from odoo import http


# class SalesReport(http.Controller):
#     @http.route('/sales_report/sales_report', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sales_report/sales_report/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sales_report.listing', {
#             'root': '/sales_report/sales_report',
#             'objects': http.request.env['sales_report.sales_report'].search([]),
#         })

#     @http.route('/sales_report/sales_report/objects/<model("sales_report.sales_report"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sales_report.object', {
#             'object': obj
#         })
