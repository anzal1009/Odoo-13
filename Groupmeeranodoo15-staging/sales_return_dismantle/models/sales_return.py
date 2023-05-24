# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.tools import float_compare, float_round
from odoo.exceptions import UserError


class SalesReturn(models.Model):
    _inherit = 'sales.return'

    dismantle_process_ids = fields.One2many('dismantle.process', 'sale_return_id', string='Dismantled Products',
                                  states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=False,
                                  auto_join=True)

    def action_return_products(self):
        super(SalesReturn, self).action_return_products()
        for record in self:
            if record.state == 'transferred':
                dismantle = []
                for line in record.return_line:
                    dismantle_dict = {
                        'product_id': line.product_id.id,
                        'product_qty': line.product_uom_qty,
                        'product_uom_id': line.product_uom.id,
                        'location_id': record.location_dest_id.id,
                        'location_dest_id': record.location_dest_id.id,
                        'lot_id': line.lot_id.id,
                        'company_id': record.company_id.id,
                        'sale_return_id': record.id,
                        'user_id': self.env.user.id
                    }
                    dismantle.append((0, 0, dismantle_dict))
                record.write({'dismantle_process_ids': dismantle})
                # for dis in record.dismantle_process_ids:
                #     dis._onchange_product_id()
                #     dis._onchange_dismantle_line()


    # def dismantle_product(self):
    #     super(SalesReturn, self).dismantle_product()
    #     for record in self:
    #         if record.dismantle_picking_id:
    #             dismantle = []
    #             for line in record.return_line:
    #                 # bom = self.env['mrp.bom'].search(['|', ('product_id', '=', line.product_id.id), '&',
    #                 #                             ('product_tmpl_id.product_variant_ids', '=', line.product_id.id),
    #                 #                             ('product_id','=',False), ('type', '=', 'normal'), '|',
    #                 #                             ('company_id', '=', line.company_id.id), ('company_id', '=', False)], limit=1)
    #                 dismantle_dict = {
    #                     'product_id': line.product_id.id,
    #                     'product_qty': line.product_uom_qty,
    #                     'product_uom_id': line.product_uom.id,
    #                     'location_id': record.dismantle_location.id,
    #                     'location_dest_id': record.location_dest_id.id,
    #                     'lot_id': line.lot_id.id,
    #                     'company_id': record.company_id.id,
    #                     'sale_return_id': record.id,
    #                     'user_id': self.env.user.id
    #                 }
    #                 dismantle.append((0, 0, dismantle_dict))
    #             record.write({'dismantle_process_ids': dismantle})
    #             for dis in record.dismantle_process_ids:
    #                 dis._onchange_product_id()
    #                 dis._onchange_dismantle_line()
    #
    # def action_view_dismantled_moves(self):
    #     pass
