# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = "res.company"

    mrp_indent_transit_location = fields.Many2one('stock.location', 'MRP Indent Transit Location',
                                                  domain="[('company_id', 'in', [id, False]), ('usage', '=', 'transit')]",
                                                  help='Default transit location used for MRP indent')
    mrp_indent_source_location = fields.Many2one('stock.location', 'MRP Indent Source Location',
                                                  domain="[('company_id', 'in', [id, False]), ('usage', '=', 'internal')]",
                                                  help='Default source location used for MRP indent')


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    mrp_indent_transit_location = fields.Many2one('stock.location', 'MRP Indent Transit Location',
                                                  domain="[('company_id', 'in', [company_id, False]), ('usage', '=', 'transit')]",
                                                  help='Default transit location used for MRP indent', readonly=False,
                                                  related='company_id.mrp_indent_transit_location')
    mrp_indent_source_location = fields.Many2one('stock.location', 'MRP Indent Source Location',
                                                  domain="[('company_id', 'in', [company_id, False]), ('usage', '=', 'internal')]",
                                                  help='Default source location used for MRP indent', readonly=False,
                                                  related='company_id.mrp_indent_source_location')
