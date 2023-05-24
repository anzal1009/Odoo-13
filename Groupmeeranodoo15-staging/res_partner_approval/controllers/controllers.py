# -*- coding: utf-8 -*-
# from odoo import http


# class ResPartnerApproval(http.Controller):
#     @http.route('/res_partner_approval/res_partner_approval', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/res_partner_approval/res_partner_approval/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('res_partner_approval.listing', {
#             'root': '/res_partner_approval/res_partner_approval',
#             'objects': http.request.env['res_partner_approval.res_partner_approval'].search([]),
#         })

#     @http.route('/res_partner_approval/res_partner_approval/objects/<model("res_partner_approval.res_partner_approval"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('res_partner_approval.object', {
#             'object': obj
#         })
