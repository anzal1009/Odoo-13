# -*- coding: utf-8 -*-
# from odoo import http


# class EasternFreebies(http.Controller):
#     @http.route('/eastern_freebies/eastern_freebies', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/eastern_freebies/eastern_freebies/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('eastern_freebies.listing', {
#             'root': '/eastern_freebies/eastern_freebies',
#             'objects': http.request.env['eastern_freebies.eastern_freebies'].search([]),
#         })

#     @http.route('/eastern_freebies/eastern_freebies/objects/<model("eastern_freebies.eastern_freebies"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('eastern_freebies.object', {
#             'object': obj
#         })
