from orca.sound import args

from odoo import http,_
from odoo.exceptions import ValidationError
from odoo.http import request
from odoo.tools import datetime


class Transfer(http.Controller):

    @http.route('/get_transfer', type='json', auth='user')
    def get_products(self):
        print("Yes here entered")
        patients_rec = request.env['stock.move'].search([])
        patients = []
        for rec in patients_rec:
            vals = {
                # 'id': rec.partner_id,
                # 'name': rec.location_id,
                'opera': rec.picking_type_id.name,
                'dest': rec.location_dest_id.name,
                'loca': rec.location_id.name,
                'name': rec.product_id.name,
                'product_id': rec.product_id.id,
                'qty': rec.product_uom_qty,
                'uom': rec.product_id.uom_id.id,
                # 'name': rec.product_id.name,
                # 'res':rec.reserved_availability,
            }
            patients.append(vals)
        print("Purchase order--->", patients)
        data = {'status': 200, 'response': patients, 'message': 'Done All Products Returned'}
        return data












    @http.route('/create_transfers', type='json', auth='user')
    def create_customer(self, **rec):
        if request.jsonrequest:
            print("rec", rec)
            if rec['name']:
                vals = {
                    'picking_type_id': rec["opera"],
                    'location_dest_id': rec['dest'],
                    'location_id': rec['loca'],
                    # 'description_picking': rec['des'],
                    'product_id': rec['product_id'],
                    'product_uom_qty': rec['qty'],
                    'product_uom': rec['uom'],
                    'name':rec['name']
                }
                new_customer = request.env['stock.move'].sudo().create(vals)
                print("New Customer Is", new_customer)
                args = {'success': True, 'message': 'Success', 'id': new_customer.id}
        return args



        # for record in self:
        #     pick_lines = []
        #     for line in record.request_line_ids:
        #         pick_line_values = {
        #             'name': line.product_id.name,
        #             'product_id': line.product_id.id,
        #             'product_uom_qty': line.product_uom_qty,
        #             'product_uom': line.product_id.uom_id.id,
        #             'state': 'draft',
        #         }
        #         pick_lines.append((0, 0, pick_line_values))
        #     picking = {
        #         'location_id': 15,
        #         'location_dest_id': record.location_dest_id.id,
        #         'move_type': 'direct',
        #         'picking_type_id': 5,
        #         'ctsrf': record.id,
        #         'move_lines': pick_lines,
        #     }
        #     transfer = self.env['stock.move'].sudo().create(picking)
        #     if transfer:
        #         record.state = 'approved'
        #         record.approved_date = datetime.Datetime.now()
        #         record.approved_by = self.env.uid
        #     else:
        #         raise ValidationError(_("Something went wrong during your Request generation"))
        # return True

















    # def create_transfer(self, **rec):
    #     if request.jsonrequest:
    #         print("rec", rec)
    #
    #         pick_lines = []
    #         pick_line_values=[]
    #         for line in range(rec):
    #             pick_line_values = {
    #                 'name': line['product_id.name'],
    #                 'product_id': line['product_id.id'],
    #                 'product_uom_qty': line['product_uom_qty'],
    #                 'product_uom': line['product_id.uom_id.id'],
    #
    #             }
    #             pick_lines.append((0, 0, pick_line_values))
    #         if rec['dest']:
    #             vals = {
    #                 'picking_type_id': 5,
    #                 'location_id': rec['loc'],
    #                 'location_dest_id': rec['dest'],
    #                 # 'move_ids_without_packages':rec
    #             }
    #             order = request.env['stock.move'].sudo().create(vals)
    #
    #     print("order Is", order)
    #     args = {'success': True, 'message': 'Success', 'id': order.id}
    #     return args
