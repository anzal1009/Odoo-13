# -*- coding: utf-8 -*-
# from odoo import http


# class ManufacturingIndent(http.Controller):
#     @http.route('/manufacturing_indent/manufacturing_indent', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/manufacturing_indent/manufacturing_indent/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('manufacturing_indent.listing', {
#             'root': '/manufacturing_indent/manufacturing_indent',
#             'objects': http.request.env['manufacturing_indent.manufacturing_indent'].search([]),
#         })

#     @http.route('/manufacturing_indent/manufacturing_indent/objects/<model("manufacturing_indent.manufacturing_indent"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('manufacturing_indent.object', {
#             'object': obj
#         })
