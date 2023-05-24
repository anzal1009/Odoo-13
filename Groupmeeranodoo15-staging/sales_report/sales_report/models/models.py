# -*- coding: utf-8 -*-

import logging
import re
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression


class ResCountryState(models.Model):
    _inherit = 'res.country.state'

    head = fields.Many2one('res.users', string='State Manager')
    regional_manager = fields.Many2one('res.users', string='Regional Manager')



class LocationArea(models.Model):
    _name = 'location.area'
    _description = 'Area'

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
    area_manager = fields.Many2one('res.users', string='Area Manager')
    users = fields.One2many('res.users','area_id', string='Users')
    state = fields.Many2one('res.country.state', string='State')
    state_manager = fields.Many2one('res.users', string='State Manager')


class ResUsers(models.Model):
    _inherit = 'res.users'

    area_id = fields.Many2one('location.area', string='Area')
    unit = fields.Float(string='Unit', default=0.00)
    value = fields.Float(string='Value', default=0.00)
    collection = fields.Float(string='Collection', default=0.00)
    sale_month_id = fields.One2many('sale.month', 'user_id', string='Month')

class ResPartner(models.Model):
    _inherit = 'res.partner'

    location_area = fields.Many2one('location.area', string='Area')
    sales_manager = fields.Many2one('res.users', string='Sales Manager')
    is_distributor = fields.Boolean(string="Is Institution",default=False)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        res= super(SaleOrder, self).onchange_partner_id()
        if self.partner_id:
            self.user_id = self.partner_id.user_id.id
        return res


