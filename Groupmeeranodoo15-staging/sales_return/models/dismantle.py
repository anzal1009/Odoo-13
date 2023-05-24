# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.tools import float_compare, float_round
from odoo.exceptions import UserError


# class DismantleProcess(models.Model):
#     _inherit = 'dismantle.process'
#
#     sale_return_id = fields.Many2one('sales.return', string='Return Reference', required=True, ondelete='cascade',
#                                      index=True, copy=False)
