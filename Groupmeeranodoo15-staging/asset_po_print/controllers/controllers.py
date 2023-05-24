# -*- coding: utf-8 -*-
# from odoo import http


# class AssetPoPrint(http.Controller):
#     @http.route('/asset_po_print/asset_po_print', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/asset_po_print/asset_po_print/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('asset_po_print.listing', {
#             'root': '/asset_po_print/asset_po_print',
#             'objects': http.request.env['asset_po_print.asset_po_print'].search([]),
#         })

#     @http.route('/asset_po_print/asset_po_print/objects/<model("asset_po_print.asset_po_print"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('asset_po_print.object', {
#             'object': obj
#         })
