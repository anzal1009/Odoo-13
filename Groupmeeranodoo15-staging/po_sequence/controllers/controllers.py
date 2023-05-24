# -*- coding: utf-8 -*-
# from odoo import http


# class PoSequence(http.Controller):
#     @http.route('/po_sequence/po_sequence', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/po_sequence/po_sequence/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('po_sequence.listing', {
#             'root': '/po_sequence/po_sequence',
#             'objects': http.request.env['po_sequence.po_sequence'].search([]),
#         })

#     @http.route('/po_sequence/po_sequence/objects/<model("po_sequence.po_sequence"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('po_sequence.object', {
#             'object': obj
#         })
