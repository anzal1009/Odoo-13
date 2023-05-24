# -*- coding: utf-8 -*-
# from odoo import http


# class InternalTransferRequest(http.Controller):
#     @http.route('/internal_transfer_request/internal_transfer_request', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/internal_transfer_request/internal_transfer_request/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('internal_transfer_request.listing', {
#             'root': '/internal_transfer_request/internal_transfer_request',
#             'objects': http.request.env['internal_transfer_request.internal_transfer_request'].search([]),
#         })

#     @http.route('/internal_transfer_request/internal_transfer_request/objects/<model("internal_transfer_request.internal_transfer_request"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('internal_transfer_request.object', {
#             'object': obj
#         })
