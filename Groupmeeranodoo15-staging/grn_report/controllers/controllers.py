# -*- coding: utf-8 -*-
# from odoo import http


# class GrnReport(http.Controller):
#     @http.route('/grn_report/grn_report', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/grn_report/grn_report/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('grn_report.listing', {
#             'root': '/grn_report/grn_report',
#             'objects': http.request.env['grn_report.grn_report'].search([]),
#         })

#     @http.route('/grn_report/grn_report/objects/<model("grn_report.grn_report"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('grn_report.object', {
#             'object': obj
#         })
