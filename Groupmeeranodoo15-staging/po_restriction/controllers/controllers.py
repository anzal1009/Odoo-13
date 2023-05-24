# -*- coding: utf-8 -*-
# from odoo import http


# class PoRestriction(http.Controller):
#     @http.route('/po_restriction/po_restriction', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/po_restriction/po_restriction/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('po_restriction.listing', {
#             'root': '/po_restriction/po_restriction',
#             'objects': http.request.env['po_restriction.po_restriction'].search([]),
#         })

#     @http.route('/po_restriction/po_restriction/objects/<model("po_restriction.po_restriction"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('po_restriction.object', {
#             'object': obj
#         })
