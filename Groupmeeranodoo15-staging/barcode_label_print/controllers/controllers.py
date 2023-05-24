# -*- coding: utf-8 -*-
# from odoo import http


# class BarcodeLabelPrint(http.Controller):
#     @http.route('/barcode_label_print/barcode_label_print', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/barcode_label_print/barcode_label_print/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('barcode_label_print.listing', {
#             'root': '/barcode_label_print/barcode_label_print',
#             'objects': http.request.env['barcode_label_print.barcode_label_print'].search([]),
#         })

#     @http.route('/barcode_label_print/barcode_label_print/objects/<model("barcode_label_print.barcode_label_print"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('barcode_label_print.object', {
#             'object': obj
#         })
