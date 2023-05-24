# -*- coding: utf-8 -*-
# from odoo import http


# class SubCutting(http.Controller):
#     @http.route('/sub_cutting/sub_cutting', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sub_cutting/sub_cutting/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sub_cutting.listing', {
#             'root': '/sub_cutting/sub_cutting',
#             'objects': http.request.env['sub_cutting.sub_cutting'].search([]),
#         })

#     @http.route('/sub_cutting/sub_cutting/objects/<model("sub_cutting.sub_cutting"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sub_cutting.object', {
#             'object': obj
#         })
