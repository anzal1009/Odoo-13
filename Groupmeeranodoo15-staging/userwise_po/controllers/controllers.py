# -*- coding: utf-8 -*-
# from odoo import http


# class UserwisePo(http.Controller):
#     @http.route('/userwise_po/userwise_po', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/userwise_po/userwise_po/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('userwise_po.listing', {
#             'root': '/userwise_po/userwise_po',
#             'objects': http.request.env['userwise_po.userwise_po'].search([]),
#         })

#     @http.route('/userwise_po/userwise_po/objects/<model("userwise_po.userwise_po"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('userwise_po.object', {
#             'object': obj
#         })
