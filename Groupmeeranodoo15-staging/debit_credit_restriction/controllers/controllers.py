# -*- coding: utf-8 -*-
# from odoo import http


# class DebitCreditRestriction(http.Controller):
#     @http.route('/debit_credit_restriction/debit_credit_restriction', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/debit_credit_restriction/debit_credit_restriction/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('debit_credit_restriction.listing', {
#             'root': '/debit_credit_restriction/debit_credit_restriction',
#             'objects': http.request.env['debit_credit_restriction.debit_credit_restriction'].search([]),
#         })

#     @http.route('/debit_credit_restriction/debit_credit_restriction/objects/<model("debit_credit_restriction.debit_credit_restriction"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('debit_credit_restriction.object', {
#             'object': obj
#         })
