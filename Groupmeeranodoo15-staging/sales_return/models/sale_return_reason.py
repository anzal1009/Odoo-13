# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleReturnReason(models.Model):
    _name = 'sale.return.reason'
    _description = 'Sale Return Reason'

    name = fields.Char(string="Reason", required=True)


class PickingType(models.Model):
    _inherit = "stock.picking.type"

    sales_return = fields.Boolean(string="Picking Type for Sales Return", default=False)


class StockLocation(models.Model):
    _inherit = "stock.location"

    dismantle_location = fields.Boolean(string="Is a dismantle Location?", default=False)
    repair_location = fields.Boolean(string="Is a Repair Location", default=False)
    resell_location = fields.Boolean(string="Is a Resell Location", default=False)

    @api.onchange('scrap_location', 'usage')
    def update_process_location(self):
        for record in self:
            if record.scrap_location or record.usage != 'internal':
                record.dismantle_location = record.repair_location = record.resell_location = False

    @api.constrains('dismantle_location', 'repair_location', 'resell_location')
    def _check_unique_scrap_process_location(self):
        locations = self.filtered(lambda location:
                                  location.scrap_location and (location.dismantle_location or
                                                               location.repair_location or location.resell_location))
        if locations:
            raise ValidationError(_("Scrap location can't be a dismantle, repair or resell location"))




