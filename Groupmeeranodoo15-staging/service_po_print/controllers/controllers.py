# -*- coding: utf-8 -*-
# from odoo import http


# class ServicePoPrint(http.Controller):
#     @http.route('/service_po_print/service_po_print', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/service_po_print/service_po_print/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('service_po_print.listing', {
#             'root': '/service_po_print/service_po_print',
#             'objects': http.request.env['service_po_print.service_po_print'].search([]),
#         })

#     @http.route('/service_po_print/service_po_print/objects/<model("service_po_print.service_po_print"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('service_po_print.object', {
#             'object': obj
#         })
