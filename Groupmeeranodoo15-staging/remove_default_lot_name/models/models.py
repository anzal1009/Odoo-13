# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    name = fields.Char(
        'Lot/Serial Number', default=False, required=True, help="Unique Lot/Serial Number", index=True)

