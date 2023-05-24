# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = "res.company"

    internal_transfer_transit_location = fields.Many2one('stock.location', 'Transit Location',
                                                  domain="[('company_id', 'in', [id, False]), ('usage', '=', 'transit')]",
                                                  help='Default transit location used for internal transfer')


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    internal_transfer_transit_location = fields.Many2one('stock.location', 'Transit Location',
                                                  domain="[('company_id', 'in', [company_id, False]), ('usage', '=', 'transit')]",
                                                  help='Default transit location used for internal transfer', readonly=False,
                                                  related='company_id.internal_transfer_transit_location')


class Users(models.Model):
    _inherit = ['res.users']

    allowed_location_ids = fields.Many2many('stock.location', relation="stock_location_users_rel", column1="user_id",
                                           column2="location_id", string='Allowed Locations', domain="[('usage', '=', 'internal')]")
