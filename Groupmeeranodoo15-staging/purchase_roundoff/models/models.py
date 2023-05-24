# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    purchase_roundoff = fields.Boolean(string='Allow rounding of purchase amount',
                                       help="Allow rounding of purchase amount")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            purchase_roundoff=params.get_param('purchase.purchase_roundoff') or False,
        )
        return res

    def set_values(self):
        self.ensure_one()
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param("purchase.purchase_roundoff", self.purchase_roundoff)


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    apply_round_off = fields.Boolean('Apply round off', default=True)
    amount_round_off = fields.Monetary(string='Round off Amount', store=True, readonly=True, compute='_amount_all')
    is_enabled_roundoff = fields.Boolean('Apply Round off', default=lambda self: self.env["ir.config_parameter"].sudo()
                                         .get_param("purchase.purchase_roundoff"))

    @api.onchange('is_enabled_roundoff')
    def onchange_is_enabled_roundoff(self):
        self._amount_all()

    @api.depends('order_line','order_line.price_total','order_line.price_subtotal',\
        'order_line.product_qty','discount_amount',\
        'discount_method','discount_type', 'order_line.discount_amount',\
        'order_line.discount_method', 'design_charge', 'freight_charge', 'packaging_forward_charge')
    def _amount_all(self):
        super(PurchaseOrder, self)._amount_all()
        for order in self:
            if order.is_enabled_roundoff:
                amount_total = round(order.amount_total)
                amount_round_off = amount_total - order.amount_total
                order.update({
                    'amount_total': amount_total,
                    'amount_round_off': amount_round_off})

