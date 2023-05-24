# -*- coding: utf-8 -*-
# from odoo import http


# class AssetSequenceUpdation(http.Controller):
#     @http.route('/asset_sequence_updation/asset_sequence_updation', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/asset_sequence_updation/asset_sequence_updation/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('asset_sequence_updation.listing', {
#             'root': '/asset_sequence_updation/asset_sequence_updation',
#             'objects': http.request.env['asset_sequence_updation.asset_sequence_updation'].search([]),
#         })

#     @http.route('/asset_sequence_updation/asset_sequence_updation/objects/<model("asset_sequence_updation.asset_sequence_updation"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('asset_sequence_updation.object', {
#             'object': obj
#         })
