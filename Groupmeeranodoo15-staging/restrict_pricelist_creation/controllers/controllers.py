# -*- coding: utf-8 -*-
# from odoo import http


# class RestrictPricelistCreation(http.Controller):
#     @http.route('/restrict_pricelist_creation/restrict_pricelist_creation', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/restrict_pricelist_creation/restrict_pricelist_creation/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('restrict_pricelist_creation.listing', {
#             'root': '/restrict_pricelist_creation/restrict_pricelist_creation',
#             'objects': http.request.env['restrict_pricelist_creation.restrict_pricelist_creation'].search([]),
#         })

#     @http.route('/restrict_pricelist_creation/restrict_pricelist_creation/objects/<model("restrict_pricelist_creation.restrict_pricelist_creation"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('restrict_pricelist_creation.object', {
#             'object': obj
#         })
