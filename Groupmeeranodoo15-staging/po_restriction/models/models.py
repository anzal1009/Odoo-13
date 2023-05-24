# -*- coding: utf-8 -*-
from odoo import models, fields, api,_
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    # def write(self, vals):
    #     if any(state == 'done' for state in set(self.mapped('state'))):
    #         raise UserError(_("No edit in done state"))
    #     else:
    #         return super().write(vals)



    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        for purchase in self:
            for po in purchase.order_line:
                if po.product_qty <= 0 or po.price_unit <= 0:
                    raise UserError(_("Zero/Negative value in Purchase order"))
        return res



