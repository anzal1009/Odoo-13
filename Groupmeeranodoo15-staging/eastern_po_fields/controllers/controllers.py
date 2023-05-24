# -*- coding: utf-8 -*-
# from odoo import http


# class EasternPoFields(http.Controller):
#     @http.route('/eastern_po_fields/eastern_po_fields', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/eastern_po_fields/eastern_po_fields/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('eastern_po_fields.listing', {
#             'root': '/eastern_po_fields/eastern_po_fields',
#             'objects': http.request.env['eastern_po_fields.eastern_po_fields'].search([]),
#         })

#     @http.route('/eastern_po_fields/eastern_po_fields/objects/<model("eastern_po_fields.eastern_po_fields"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('eastern_po_fields.object', {
#             'object': obj
#         })
