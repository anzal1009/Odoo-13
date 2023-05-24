# -*- coding: utf-8 -*-
# from odoo import http


# class RemoveDefaultLotName(http.Controller):
#     @http.route('/remove_default_lot_name/remove_default_lot_name', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/remove_default_lot_name/remove_default_lot_name/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('remove_default_lot_name.listing', {
#             'root': '/remove_default_lot_name/remove_default_lot_name',
#             'objects': http.request.env['remove_default_lot_name.remove_default_lot_name'].search([]),
#         })

#     @http.route('/remove_default_lot_name/remove_default_lot_name/objects/<model("remove_default_lot_name.remove_default_lot_name"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('remove_default_lot_name.object', {
#             'object': obj
#         })
