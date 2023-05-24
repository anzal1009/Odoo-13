# -*- coding: utf-8 -*-
# from odoo import http


# class SaleInvoiceReport(http.Controller):
#     @http.route('/sale_invoice_report/sale_invoice_report', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_invoice_report/sale_invoice_report/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_invoice_report.listing', {
#             'root': '/sale_invoice_report/sale_invoice_report',
#             'objects': http.request.env['sale_invoice_report.sale_invoice_report'].search([]),
#         })

#     @http.route('/sale_invoice_report/sale_invoice_report/objects/<model("sale_invoice_report.sale_invoice_report"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_invoice_report.object', {
#             'object': obj
#         })
