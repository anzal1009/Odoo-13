# -*- coding: utf-8 -*-
# from odoo import http


# class RestrictJeCashBank(http.Controller):
#     @http.route('/restrict_je_cash_bank/restrict_je_cash_bank', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/restrict_je_cash_bank/restrict_je_cash_bank/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('restrict_je_cash_bank.listing', {
#             'root': '/restrict_je_cash_bank/restrict_je_cash_bank',
#             'objects': http.request.env['restrict_je_cash_bank.restrict_je_cash_bank'].search([]),
#         })

#     @http.route('/restrict_je_cash_bank/restrict_je_cash_bank/objects/<model("restrict_je_cash_bank.restrict_je_cash_bank"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('restrict_je_cash_bank.object', {
#             'object': obj
#         })
