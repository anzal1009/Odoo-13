# -*- coding: utf-8 -*-
# from odoo import http


# class AssetSequenceNumber(http.Controller):
#     @http.route('/asset_sequence_number/asset_sequence_number', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/asset_sequence_number/asset_sequence_number/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('asset_sequence_number.listing', {
#             'root': '/asset_sequence_number/asset_sequence_number',
#             'objects': http.request.env['asset_sequence_number.asset_sequence_number'].search([]),
#         })

#     @http.route('/asset_sequence_number/asset_sequence_number/objects/<model("asset_sequence_number.asset_sequence_number"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('asset_sequence_number.object', {
#             'object': obj
#         })
