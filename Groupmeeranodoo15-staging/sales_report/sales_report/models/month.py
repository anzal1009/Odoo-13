# -*- coding: utf-8 -*-

import logging
import re
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression
from dateutil.relativedelta import relativedelta
import datetime
from datetime import datetime,date



class DRSRMONTH(models.Model):
    _name = 'sale.month'
    _description = 'Month'

    name = fields.Selection([
        ('1', 'January'),
        ('2', 'February'),
        ('3', 'March'),
        ('4', 'April'),
        ('5', 'May'),
        ('6', 'June'),
        ('7', 'July'),
        ('8', 'August'),
        ('9', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December')],
        string='Month',)
    unit = fields.Float(string='Unit', default=0.00)
    value = fields.Float(string='Value', default=0.00)
    collection = fields.Float(string='Collection', default=0.00)
    user_id = fields.Many2one('res.users',string="Users")
    # first_date = fields.Date(string='Starting Date',default=fields.Date.context_today)
    # start_date = fields.Date('Start Period', required=True)
    # end_date = fields.Date('End Period', required=True)

    # def get_years(self):
    #     return [(i, str(i)) for i in range(2019, 2030)]
        # year_list = []
        # for i in range(2019, 2030):
        #     year_list.append((i, str(i)))
        # return year_list

    year = fields.Selection(selection=[
        ('2019', '2019'),
        ('2020', '2020'),
        ('2021', '2021'),
        ('2022', '2022'),
        ('2023', '2023'),
        ('2024', '2024'),
        ('2025', '2025'),
        ('2026', '2026'),
        ('2027', '2027'),
        ('2028', '2028'),
        ('2029', '2029'),
        ('2030', '2030')], string='Year')


    # @api.onchange('name','year')
    # def _starting_date(self):
    #     for day in self:
    #         month_val = date.today().month
    #         year_val = date.today().year
    #         if day.year:
    #             year_val = day.year
    #         if day.name:
    #             month_val = day.name
    #         else:
    #             month_val = date.today().month
    #             year_val = date.today().year
    #
    #         day.first_date = date(year=int(year_val), month=int(month_val),day=int(1))
    #     return



