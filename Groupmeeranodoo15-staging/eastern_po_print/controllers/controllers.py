# -*- coding: utf-8 -*-
# from odoo import http


# class EasternPoPrint(http.Controller):
#     @http.route('/eastern_po_print/eastern_po_print', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/eastern_po_print/eastern_po_print/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('eastern_po_print.listing', {
#             'root': '/eastern_po_print/eastern_po_print',
#             'objects': http.request.env['eastern_po_print.eastern_po_print'].search([]),
#         })

#     @http.route('/eastern_po_print/eastern_po_print/objects/<model("eastern_po_print.eastern_po_print"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('eastern_po_print.object', {
#             'object': obj
#         })
