# -*- coding: utf-8 -*-
# from odoo import http


# class PurchaseRoundoff(http.Controller):
#     @http.route('/purchase_roundoff/purchase_roundoff', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/purchase_roundoff/purchase_roundoff/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('purchase_roundoff.listing', {
#             'root': '/purchase_roundoff/purchase_roundoff',
#             'objects': http.request.env['purchase_roundoff.purchase_roundoff'].search([]),
#         })

#     @http.route('/purchase_roundoff/purchase_roundoff/objects/<model("purchase_roundoff.purchase_roundoff"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('purchase_roundoff.object', {
#             'object': obj
#         })
