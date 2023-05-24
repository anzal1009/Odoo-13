# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def create(self, values):
        if self.env.user.has_group('res_partner_approval.group_hide_partner_creation'):
            raise UserError(_('You are not allowed to create partner. Please contact Administrator.'))
        return super(ResPartner, self).create(values)

    # def write(self, values):
    #     if self.env.user.has_group('res_partner_approval.group_hide_partner_creation'):
    #         raise UserError(_('You are not allowed to edit this partner. Please contact Administrator.'))
    #     return super(ResPartner, self).write(values)

    def unlink(self):
        if self.env.user.has_group('res_partner_approval.group_hide_partner_creation'):
            raise UserError(_('You are not allowed to delete this partner. Please contact Administrator.'))
        else:
            return super(ResPartner, self).unlink()

    def toggle_active(self):
        for order in self:
            if self.env.user.has_group('res_partner_approval.group_hide_partner_creation'):
                raise UserError(_('You can not archive/ unarchive this partner. Please contact Administrator.'))
            return super(ResPartner, order).toggle_active()

    # def name_get(self):
    #     res = []
    #     for partner in self.filtered(lambda picking: picking.vat):
    #         name = partner._get_name()
    #         res.append((partner.id, name))
    #     return res
    #
    # @api.model
    # def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
    #     # args.append([('vat', '!=', False)])
    #     if not args:
    #         args = [['vat', '!=', False]]
    #     else:
    #         args.append(['vat', '!=', False])
    #     res = super(ResPartner, self)._name_search(name, args=args, operator=operator, limit=limit,
    #                                                name_get_uid=name_get_uid)
    #     return res
#
#     @api.model
#     def search(self, args, offset=0, limit=None, order=None, count=False):
