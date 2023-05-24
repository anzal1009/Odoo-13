# -*- coding: utf-8 -*-
# from odoo import http


# class InvoicePrintWarehouseAddress(http.Controller):
#     @http.route('/invoice_print_warehouse_address/invoice_print_warehouse_address', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/invoice_print_warehouse_address/invoice_print_warehouse_address/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('invoice_print_warehouse_address.listing', {
#             'root': '/invoice_print_warehouse_address/invoice_print_warehouse_address',
#             'objects': http.request.env['invoice_print_warehouse_address.invoice_print_warehouse_address'].search([]),
#         })

#     @http.route('/invoice_print_warehouse_address/invoice_print_warehouse_address/objects/<model("invoice_print_warehouse_address.invoice_print_warehouse_address"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('invoice_print_warehouse_address.object', {
#             'object': obj
#         })
