# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError,AccessError



class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'


    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        # for purchase in self:
        if not self.env.user.has_group('userwise_po.group_purchase_order_approver'):
            raise AccessError(_("You don't have the access rights to Confirm a Puchase Order."))
        return res