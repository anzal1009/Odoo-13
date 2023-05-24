# -*- coding: utf-8 -*-
# from odoo import http


# class CustomCreditNotePrint(http.Controller):
#     @http.route('/custom_credit_note_print/custom_credit_note_print/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_credit_note_print/custom_credit_note_print/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_credit_note_print.listing', {
#             'root': '/custom_credit_note_print/custom_credit_note_print',
#             'objects': http.request.env['custom_credit_note_print.custom_credit_note_print'].search([]),
#         })

#     @http.route('/custom_credit_note_print/custom_credit_note_print/objects/<model("custom_credit_note_print.custom_credit_note_print"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_credit_note_print.object', {
#             'object': obj
#         })
