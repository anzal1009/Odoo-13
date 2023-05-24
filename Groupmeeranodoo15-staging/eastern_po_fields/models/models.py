# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    pan = fields.Char('PAN')
    cin = fields.Char('CIN')


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    freight = fields.Char('Freight')
    document = fields.Char('Documents')
    advance = fields.Char('Advance')
    other_document1 = fields.Char('Others 1')
    other_document2 = fields.Char('Others 2')
    kind_attention = fields.Html('Kind Attention')
    special_instruction = fields.Html('Special Instruction')
    other_instruction = fields.Html('Other Instruction')
    bill_to_partner_id = fields.Many2one('stock.warehouse', string="Bill To")

    design_charge = fields.Float(string='Design Charge', digits='Product Price', default=0.0)
    freight_charge = fields.Float(string='Freight Charge', digits='Product Price', default=0.0)
    packaging_forward_charge = fields.Float(string='Packaging & Forward Charge', digits='Product Price', default=0.0)
    design_charge_amt = fields.Monetary(compute='_amount_all', string='Design Charge', store=True)
    freight_charge_amt = fields.Monetary(compute='_amount_all', string='Freight Charge', store=True)
    packaging_forward_charge_amt = fields.Monetary(compute='_amount_all', string='Packaging & Forward Charge', store=True)

    @api.depends('order_line','order_line.price_total','order_line.price_subtotal',\
        'order_line.product_qty','discount_amount',\
        'discount_method','discount_type', 'order_line.discount_amount',\
        'order_line.discount_method', 'design_charge', 'freight_charge', 'packaging_forward_charge')
    def _amount_all(self):
        super(PurchaseOrder, self)._amount_all()
        for order in self:
            amount_total = order.amount_total + order.design_charge + order.freight_charge + order.packaging_forward_charge
            order.update({
                'amount_total': amount_total,
                'design_charge_amt': order.design_charge,
                'freight_charge_amt': order.freight_charge,
                'packaging_forward_charge_amt': order.packaging_forward_charge
            })



