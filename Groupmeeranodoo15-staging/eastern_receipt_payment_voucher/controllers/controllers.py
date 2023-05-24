# -*- coding: utf-8 -*-
# from odoo import http


# class EmdadReceiptVoucher(http.Controller):
#     @http.route('/emdad_receipt_voucher/emdad_receipt_voucher', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/emdad_receipt_voucher/emdad_receipt_voucher/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('emdad_receipt_voucher.listing', {
#             'root': '/emdad_receipt_voucher/emdad_receipt_voucher',
#             'objects': http.request.env['emdad_receipt_voucher.emdad_receipt_voucher'].search([]),
#         })

#     @http.route('/emdad_receipt_voucher/emdad_receipt_voucher/objects/<model("emdad_receipt_voucher.emdad_receipt_voucher"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('emdad_receipt_voucher.object', {
#             'object': obj
#         })
