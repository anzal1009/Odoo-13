# -*- coding: utf-8 -*-
# from odoo import http


# class MsmePartner(http.Controller):
#     @http.route('/msme_partner/msme_partner', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/msme_partner/msme_partner/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('msme_partner.listing', {
#             'root': '/msme_partner/msme_partner',
#             'objects': http.request.env['msme_partner.msme_partner'].search([]),
#         })

#     @http.route('/msme_partner/msme_partner/objects/<model("msme_partner.msme_partner"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('msme_partner.object', {
#             'object': obj
#         })
