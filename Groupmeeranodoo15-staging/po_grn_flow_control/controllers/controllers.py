# -*- coding: utf-8 -*-
# from odoo import http


# class PoGrnFlowControl(http.Controller):
#     @http.route('/po_grn_flow_control/po_grn_flow_control', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/po_grn_flow_control/po_grn_flow_control/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('po_grn_flow_control.listing', {
#             'root': '/po_grn_flow_control/po_grn_flow_control',
#             'objects': http.request.env['po_grn_flow_control.po_grn_flow_control'].search([]),
#         })

#     @http.route('/po_grn_flow_control/po_grn_flow_control/objects/<model("po_grn_flow_control.po_grn_flow_control"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('po_grn_flow_control.object', {
#             'object': obj
#         })
