# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class RepairComponents(models.Model):
    _name = 'repair.components'
    _description = 'Products needed for repair'
    _order = 'sale_return_id, id'
    _check_company_auto = True

    sale_return_id = fields.Many2one('sales.return', string='Return Reference', required=True, ondelete='cascade',
                                     index=True, copy=False)
    company_id = fields.Many2one(related='sale_return_id.company_id', string='Company', store=True, index=True)
    product_id = fields.Many2one('product.product', string='Product', change_default=True, ondelete='cascade',
                                 domain="[('type', '!=', 'service'), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
                                 check_company=True)
    product_uom = fields.Many2one('uom.uom', 'Unit of Measure', required=True,
                                     domain="[('category_id', '=', product_uom_category_id)]", ondelete="restrict")
    product_uom_qty = fields.Float(string='Quantity', digits='Product Unit of Measure', required=True, default=1.0)
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')

    lot_id = fields.Many2one(
        'stock.production.lot', 'Lot/Serial Number',
        domain="[('product_id', '=', product_id), ('company_id', '=', company_id)]", check_company=True)
    product_reference = fields.Char('Product Reference', )
    tracking = fields.Selection(string='Product Tracking', readonly=True, related="product_id.tracking")

    date = fields.Datetime('Date', default=fields.Datetime.now, required=True)
    user_id = fields.Many2one(related='sale_return_id.user_id', store=True, string='User')
    # process = fields.Selection(related='sale_return_id.process', store=True, string='Process')

    @api.onchange('product_id')
    def product_id_change(self):
        if not self.product_id:
            return
        vals = {}
        if not self.product_uom or (self.product_id.uom_id.id != self.product_uom.id):
            vals['product_uom'] = self.product_id.uom_id
            vals['product_uom_qty'] = self.product_uom_qty or 1.0
        vals['product_reference'] = self.product_id.default_code
        self.update(vals)












