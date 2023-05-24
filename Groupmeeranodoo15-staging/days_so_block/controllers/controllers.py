# -*- coding: utf-8 -*-
# from odoo import http


# class DaysSoBlock(http.Controller):
#     @http.route('/days_so_block/days_so_block', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/days_so_block/days_so_block/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('days_so_block.listing', {
#             'root': '/days_so_block/days_so_block',
#             'objects': http.request.env['days_so_block.days_so_block'].search([]),
#         })

#     @http.route('/days_so_block/days_so_block/objects/<model("days_so_block.days_so_block"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('days_so_block.object', {
#             'object': obj
#         })
