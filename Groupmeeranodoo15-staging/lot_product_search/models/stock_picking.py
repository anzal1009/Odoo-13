# -*- coding: utf-8 -*-

from odoo import models, fields, api
# name_search_keyword = []


class Picking(models.Model):
    _inherit = 'stock.picking'

    lot_serial_no = fields.Char(string="Lot/Serial No", placeholder="lot/serial no search")

    @api.onchange('lot_serial_no')
    def onchange_lot_serial_no_load_product(self):
        if not self.lot_serial_no:
            return {}
        lot_no = self.env['stock.production.lot'].search([('name', 'ilike', self.lot_serial_no)], limit=1)
        self.move_line_ids_without_package = [(0, 0,  {
            'product_id': lot_no.product_id.id,
            'product_uom_id': lot_no.product_id.uom_id.id,
            'lot_id': lot_no.id,
            'picking_id': self.id,
            'qty_done': 1,
            'location_id': self.location_id.id,
            'location_dest_id': self.location_dest_id.id
        })]
        self.lot_serial_no = False
