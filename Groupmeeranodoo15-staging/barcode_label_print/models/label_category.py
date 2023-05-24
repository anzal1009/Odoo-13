# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict

from odoo import _, models,fields
from odoo.exceptions import UserError
class LabelCategory(models.Model):
    _name = 'label.category'
    _description = 'Label Category'

    name = fields.Char(string="Name")
    # code = fields.Char(string="Code")
