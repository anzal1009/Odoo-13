# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class Pricelist(models.Model):
    _inherit = 'product.pricelist'

    @api.model
    def create(self, values):
        if self.env.user.has_group('restrict_pricelist_creation.group_hide_pricelist_creation'):
            raise UserError(_('You are not allowed to create pricelist. Please contact Administrator.'))
        return super(Pricelist, self).create(values)

    def write(self, values):
        if self.env.user.has_group('restrict_pricelist_creation.group_hide_pricelist_creation'):
            raise UserError(_('You are not allowed to edit this pricelist. Please contact Administrator.'))
        return super(Pricelist, self).write(values)

    def unlink(self):
        if self.env.user.has_group('restrict_pricelist_creation.group_hide_pricelist_creation'):
            raise UserError(_('You are not allowed to delete this pricelist. Please contact Administrator.'))
        else:
            return super(Pricelist, self).unlink()

    def toggle_active(self):
        for order in self:
            if self.env.user.has_group('restrict_pricelist_creation.group_hide_pricelist_creation'):
                raise UserError(_('You can not archive/ unarchive this pricelist. Please contact Administrator.'))
            return super(Pricelist, order).toggle_active()
