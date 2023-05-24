# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

import base64
from io import StringIO
from odoo import api, fields, models
from datetime import date
from odoo.tools.float_utils import float_round
from odoo.exceptions import Warning
from xlsxwriter.utility import xl_range, xl_rowcol_to_cell
from itertools import groupby
import itertools
from collections import OrderedDict,defaultdict
import json
from operator import itemgetter
from dateutil.relativedelta import relativedelta
from datetime import date




import io

try:
    import xlwt
except ImportError:
    xlwt = None


class sale_report_wizard(models.TransientModel):
    _name = "sale.report.wizard"
    _description = "DSR Report Wizard"

    start_date = fields.Date('Start Period', required=True)
    end_date = fields.Date('End Period', required=True)
    company_id = fields.Many2one('res.company', string='Company',required=True)


    # def print_report(self):
    #     datas = {
    #         'ids': self._ids,
    #         'model': 'sales.report.wizard',
    #         'start_date': self.start_date,
    #         'end_date': self.end_date,
    #         'company_id': self.company_id,
    #     }
    #     return self.env.ref('sales_report.sale_report_template_pdf').report_action(
    #         self)

    def get_regional_manager(self):
        state_manager = self.env['res.country.state'].search([])
        manager = [managers for managers in state_manager if managers.regional_manager]
        return manager
    def get_state_head(self):
        state_head = self.env['res.country.state'].search([])
        head = [managers for managers in state_head if managers.head]
        return head

    def set_group_by_area_manager(self,lines):

        # tmp = defaultdict(list)
        list_values = sorted(lines,key=itemgetter('area_manager'))
        lines_val = OrderedDict((k, [m for m in v]) for k, v in groupby(list_values,key=itemgetter('area_manager')) if k!=0)
        # group_lines = itertools.groupby(lines, key=lambda x: (x['area_manager']))
        # lines_val = OrderedDict((k, [m for m in v]) for k, v in group_lines)
        lines_val = json.loads(json.dumps(lines_val))
        if lines_val.get('0'):
            del lines_val['0']
        return lines_val

    def set_group_by_state_manager(self,lines):
        # group_lines = itertools.groupby(lines, key=lambda x: (x['state_manager']))
        # lines = OrderedDict((k, [m['area_manager'] for m in v]) for k, v in group_lines)
        list_values = sorted(lines, key=itemgetter('state_manager'))
        lines_val = OrderedDict((k, [m['area_manager'] for m in v]) for k, v in groupby(list_values, key=itemgetter('state_manager')))
        lines_val = json.loads(json.dumps(lines_val))
        if lines_val.get('0'):
            del lines_val['0']
        return lines_val
        # temp = []
        # res = dict()
        # for key, vals in lines.items():
        #     for val in vals:
        #         if val not in temp:
        #             temp.append(val)
        #             res[key] = val
        # return res

    def set_group_by_regional_manager(self,lines):
        list_values = sorted(lines, key=itemgetter('regional_manager'))
        lines_val = OrderedDict((k, [m['state_manager'] for m in v]) for k, v in groupby(list_values, key=itemgetter('regional_manager')))
        lines_val = json.loads(json.dumps(lines_val))
        if lines_val.get('0'):
            del lines_val['0']
        return lines_val
        # group_lines = itertools.groupby(lines, key=lambda x: (x['regional_manager']))
        # lines = OrderedDict((k, [m['state_manager'] for m in v]) for k, v in group_lines)
        # lines = json.loads(json.dumps(lines))
        # return lines

    def _financial_year_values(self):
        date_from = self.start_date
        date_to = self.end_date
        company_id = self.company_id
        current_year = date.today().year

        financial_period = date(year=int(current_year), month=int(self.company_id.fiscalyear_last_month),
                                day=int(self.company_id.fiscalyear_last_day)) + relativedelta(days=1) \
                           + relativedelta(year=int(current_year))

        list_of_month = []
        list_of_year = []
        ytd_month = ytd_year = []
        for months in range(date_from.month, (date_to.month + 1)):
            list_of_month.append(months)
        for fin_years in range(financial_period.year, (date_to.year + 1)):
            ytd_year.append(fin_years)
        for fin_months in range(financial_period.month, (date_to.month + 1)):
            ytd_month.append(fin_months)
        for years in range(date_from.year, (date_to.year + 1)):
            list_of_year.append(years)
        return list_of_year,list_of_month,ytd_year,ytd_month


    def get_company(self):

        if self.company_id:
            l1 = []
            l2 = []
            obj = self.env['res.company'].search([('id', '=', self.company_id.id)])
            l1.append(obj.name)
            return l1


    def print_exl_report(self):
        if xlwt:
            data = {'start_date': self.start_date,
                    'end_date': self.end_date,
                    'company_id': self.company_id.name,
                    }
            filename = 'DSR Report.xls'
            l1 = []
            get_company = self.get_company()
            workbook = xlwt.Workbook()
            stylePC = xlwt.XFStyle()
            alignment = xlwt.Alignment()
            alignment.horz = xlwt.Alignment.HORZ_CENTER
            fontP = xlwt.Font()
            fontP.bold = True
            fontP.height = 200

            # xlwt.add_palette_colour("custom_colour", 0x21)
            # workbook.set_colour_RGB(0x21, 131, 242, 122)
            # xlwt.add_palette_colour("second_colour", 0x21)
            # workbook.set_colour_RGB(0x21, 146, 208, 80)

            stylePC.font = fontP
            stylePC.num_format_str = '@'
            stylePC.alignment = alignment
            style_title = xlwt.easyxf(
                "font:height 500; font: name Liberation Sans, bold on,color blue; align: horiz center;")
            style_table_header = xlwt.easyxf(
                "font:height 200; font: name Liberation Sans, bold on,color black; align: horiz center")
            style = xlwt.easyxf("font:height 200; font: name Liberation Sans,color black;align: horiz right;")
            style1 = xlwt.easyxf("font:height 200; font: name Liberation Sans,color black;")

            format0 = xlwt.easyxf(
                'font:height 200,bold True;pattern: pattern solid, fore_colour lime;align: horiz center; borders: top_color black, bottom_color black, right_color black, left_color black,\
                left thin, right thin, top thin, bottom thin;'
            )
            format1 = xlwt.easyxf(
                'font:height 200,bold True;pattern: pattern solid, fore_colour yellow;font: name Liberation Sans,color black;align: horiz right;'

            )
            format11 = xlwt.easyxf(
                'font:height 200,bold True;pattern: pattern solid, fore_colour yellow;font: name Liberation Sans,color black;'

            )
            format2 = xlwt.easyxf(
                'align: horiz right;font:height 200,bold True;pattern: pattern solid, fore_colour light_green;font: name Liberation Sans,color black;'

            )
            format21 = xlwt.easyxf(
                'font:height 200,bold True;pattern: pattern solid, fore_colour light_green;font: name Liberation Sans,color black;'

            )
            format31 = xlwt.easyxf(
                'font:height 200,bold True;pattern: pattern solid, fore_colour lime;font: name Liberation Sans,color black;'

            )
            format3 = xlwt.easyxf(
                'align: horiz right;font:height 200,bold True;pattern: pattern solid, fore_colour lime;font: name Liberation Sans,color black;'

            )
            worksheet = workbook.add_sheet('Sheet 1')
            worksheet.col(0).width = 2000
            worksheet.row(8).height = 500
            worksheet.row(9).height = 500
            worksheet.col(1).width = 5120
            worksheet.col(2).width = 5120
            worksheet.col(3).width = 7000
            worksheet.col(4).width = 5120
            worksheet.col(5).width = 5120
            worksheet.col(6).width = 5120  # sets the cell width
            worksheet.write(5, 1, 'Start Date:', style_table_header)
            worksheet.write(6, 1, str(self.start_date))
            worksheet.write(5, 2, 'End Date', style_table_header)
            worksheet.write(6, 2, str(self.end_date))
            worksheet.write(5, 3, 'Company', style_table_header)
            worksheet.write(6, 3, get_company and get_company[0] or '', )

            w_col_no = 7
            w_col_no1 = 8

            worksheet.write_merge(0, 1, 0, 19, "DSR REPORT", style=style_title)

            worksheet.write_merge(8, 9, 0, 0, 'Sl No', format0)
            worksheet.write_merge(8,9,1,1, 'Name', format0)
            worksheet.write_merge(8,9,2,2, 'Area', format0)
            worksheet.write_merge(8,9,3,3, 'Distributor', format0)

            worksheet.write_merge(8, 8, 4, 5, 'Carry Forward', format0)
            worksheet.write(9, 4, 'Units', format0)
            worksheet.write(9, 5, 'Value', format0)

            worksheet.write_merge(8, 8, 6, 8, 'Target', format0)
            worksheet.write(9,6, 'Units', format0)
            worksheet.write(9,7, 'Value', format0)
            worksheet.write(9,8, 'Collection', format0)

            worksheet.write_merge(8, 8, 9, 11, 'FTD Achievement- Order', format0)
            worksheet.write(9,9, 'Units', format0)
            worksheet.write(9,10, 'Value', format0)
            worksheet.write(9,11, 'Collection', format0)

            worksheet.write_merge(8, 8, 12, 14, 'MTD Achievement - Order', format0)
            worksheet.write(9,12, 'Units', format0)
            worksheet.write(9,13, 'Value', format0)
            worksheet.write(9,14, '%', format0)

            worksheet.write_merge(8, 8, 15, 21, 'MTD Achievement - Dispatch', format0)
            worksheet.write(9,15, 'Units', format0)
            worksheet.write(9,16, '%', format0)
            worksheet.write(9,17, 'Value', format0)
            worksheet.write(9,18, '%', format0)
            worksheet.write(9,19, 'NRV', format0)
            worksheet.write(9,20, 'Collection', format0)

            # worksheet.write(8,19, '', format0)
            worksheet.write(9,21, '%', format0)

            worksheet.write_merge(8, 9, 22,22, 'YTD Target', format0)
            worksheet.write_merge(8, 9, 23,23, 'YTD Achivement', format0)

            # worksheet.write(9, 22, 'YTD Target', format0)
            # worksheet.write(9, 23, 'YTD Achivement', format0)




            prod_row = 10

            prod_col = 0
            lines = []

            date_from = self.start_date
            date_to = self.end_date
            company_id = self.company_id

            current_year = date.today().year

            financial_period =  date(year=int(current_year),month=int(self.company_id.fiscalyear_last_month),
                 day=int(self.company_id.fiscalyear_last_day)) + relativedelta(days=1)\
                                +relativedelta(year=int(current_year))

            list_of_month=[]
            list_of_year=[]
            ytd_month=ytd_year=[]
            for months in range(date_from.month,(date_to.month+1)):
                list_of_month.append(months)
                # list_of_month = map(str, list_of_month)

            for fin_years in range(financial_period.year,(date_to.year+1)):
                ytd_year.append(fin_years)

            for fin_months in range(financial_period.month, (date_to.month + 1)):
                ytd_month.append(fin_months)
                # list_of_month = map(str, list_of_month)

            for years in range(date_from.year, (date_to.year + 1)):
                list_of_year.append(years)

            sl = 0



            query = '''


            select              d.mtd_dispatch_units,
                        d.mtd_dispatch_value,
                        d.mtd_dispatch_collection,
                        d.mtd_unit,
                        d.mtd_value,
                        d.ftd_value,
                        d.ftd_unit,
                        d.ftd_collection,
                        --d.user_id,
                         (CASE WHEN d.user_id is null THEN d.id ELSE d.user_id END) as user_id,
                   -- d.user_id as user_id,
                        d.carry_forward_value,
                        d.carry_forward_unit,
                        d.user_target_unit as user_units,
                        d.user_target_value as user_value,
                        d.user_target_collection as user_collection,
                        d.distributor,
                        d.sale_partner_id,
                        d.financial_target_collection as ytd_target_collection,
                        d.financial_target_value as ytd_target,
                        d.ytd_user_value,
                        d.user_area
                  from (
                  

            	(select max(CASE WHEN rs.is_distributor is null THEN rs.name ELSE ' ' END) as distributor,max(s.id) as sale_partner_id,max(ru.area_id) as user_area,
             	sum(CASE WHEN pp.freebie=false or pp.freebie is null THEN (sl.product_uom_qty) ELSE 0.0 END) as mtd_unit,
                 sum(CASE WHEN pp.freebie=false or pp.freebie is null THEN (sl.product_uom_qty-sl.qty_delivered) ELSE 0.0 END) as carry_forward_unit,
                 sum((sl.product_uom_qty-sl.qty_delivered)*sl.price_unit) as carry_forward_value,

                 sum(CASE WHEN to_char(date_trunc('day',s.date_order),'YYYY-MM-DD')::date  = %s and (pp.freebie=false or pp.freebie is null) THEN (sl.product_uom_qty) ELSE 0.0 END) as ftd_unit,
                 sum(CASE WHEN to_char(date_trunc('day',s.date_order),'YYYY-MM-DD')::date  = %s  THEN (sl.product_uom_qty*sl.price_unit) ELSE 0.0 END) as ftd_value,

				 
				  sum(CASE WHEN to_char(date_trunc('day',s.date_order),'YYYY-MM-DD')::date  = %s  THEN (s.amount_total) ELSE 0.0 END) as ftd_collections,


             		sum(sl.product_uom_qty*sl.price_unit) as mtd_value,s.user_id
             	from sale_order_line as sl
            		left join sale_order as s on s.id=sl.order_id
                     LEFT JOIN product_product pp on pp.id=sl.product_id
            		left join res_partner as rs on rs.id=s.partner_id
            		left join res_users as ru on ru.id=s.user_id
            	where to_char(date_trunc('day',s.date_order),'YYYY-MM-DD')::date between %s and %s
            	and s.state in ('sale','done')
            	and s.company_id =%s
            	group by s.user_id)a 
            	
            	        -- on a.user_id=r.id
            	
            		left join



            	(SELECT sum(aml.price_subtotal) as mtd_dispatch_value,
                         so.user_id AS user_id_val,   
                           sum(am.amount_total) AS mtd_dispatch_collections,    
                          sum(CASE WHEN pp.freebie=false or pp.freebie is null THEN (aml.quantity) ELSE 0.0 END) as mtd_dispatch_units
                    FROM sale_order so
                    JOIN sale_order_line sol ON sol.order_id = so.id
					LEFT JOIN product_product pp on pp.id=sol.product_id
                    JOIN sale_order_line_invoice_rel soli_rel ON soli_rel.order_line_id = sol.id
                    JOIN account_move_line aml ON aml.id = soli_rel.invoice_line_id
                    JOIN account_move am ON am.id = aml.move_id
                WHERE
                    am.move_type in ('out_invoice', 'out_refund') 
					and  to_char(date_trunc('day',so.date_order),'YYYY-MM-DD')::date between %s and %s
                           and so.company_id =%s
                           group by so.user_id)c
                                 on a.user_id=c.user_id_val

                                          left join
                      (
                
                         select sum(p.amount) as mtd_dispatch_collection,
                          sum(CASE WHEN to_char(date_trunc('day',m.date),'YYYY-MM-DD')::date  = %s  THEN (p.amount) ELSE 0.0 END) as ftd_collection,
                            rs.id as user_id_payment from account_payment as p
                          left join account_move as m on p.move_id = m.id
                          left join res_partner as rp on rp.id=p.partner_id
                          left join res_users as rs on rs.id= rp.user_id                          
                          where to_char(date_trunc('day',m.date),'YYYY-MM-DD'):: date between %s and %s
                          and m.company_id =%s
                          and state in ('posted') and partner_type='customer' group by rs.id
                      )e
                      
                      on a.user_id=e.user_id_payment
                      
                      
                      left join
                      
                      (
                      select sum(collection) as user_target_collection,sum(unit) as user_target_unit,
                      sum(value) as user_target_value,
                      user_id as target_user_id from sale_month
                    where (name in %s and year in %s ) group by user_id
                      )f on f.target_user_id= a.user_id
                      
                      left join 
                      
                       (
                      select sum(collection) as financial_target_collection,sum(unit) as financial_target_unit,
                      sum(value) as financial_target_value,
                      user_id as financial_user_id from sale_month
                    where (name in %s and year in %s ) group by user_id
                      )g on g.financial_user_id= a.user_id
                      
                      
                      left join 
                      
                      
                      	(
                      	SELECT 
                       sum(CASE WHEN (pp.freebie=false or pp.freebie is null) THEN (sol.price_subtotal) ELSE 0.0 END) as ytd_user_value,
                         so.user_id AS ytd_user_id,   
                           sum(so.amount_total) AS ytd_user_collection    
                          from stock_move_line ml
                           JOIN stock_move m ON m.id = ml.move_id
                           JOIN sale_order_line sol ON sol.id = m.sale_line_id
                           JOIN sale_order so ON so.id = sol.order_id
                           LEFT JOIN product_product pp on pp.id=sol.product_id
                           WHERE  m.state in ('confirmed', 'done')
                           and  to_char(date_trunc('day',so.date_order),'YYYY-MM-DD')::date between %s and %s
                           and so.company_id =%s
                           group by so.user_id)k on a.user_id=k.ytd_user_id
                      
                                 
                            
                                  full join (select u.id as id
                                from res_users as u
                                group by u.id)z on z.id= a.user_id 

				  )d

                                                                          '''

            self.env.cr.execute(query, (
                date_to,date_to,date_to,
                date_from, date_to, company_id.id,
                date_from, date_to, company_id.id,
                date_to,date_from, date_to, company_id.id,
                tuple(map(str, list_of_month)),tuple(map(str, list_of_year)),
                tuple(map(str, ytd_month)), tuple(map(str, ytd_year)),
                financial_period, date_to, company_id.id,

            ))
            for row in self.env.cr.dictfetchall():
                sl += 1

                user_name = row['user_id'] if row['user_id'] else 0
                user_area = row['user_area'] if row['user_area'] else ""
                carry_forward_value = row['carry_forward_value'] if row['carry_forward_value'] else 0.0
                carry_forward_unit = row['carry_forward_unit'] if row['carry_forward_unit'] else 0.0
                # distributor = row['distributor'] if row['distributor'] else ""
                mtd_dispatch_collection = row['mtd_dispatch_collection'] if row['mtd_dispatch_collection'] else 0.0
                ytd_target = row['ytd_target'] if row['ytd_target'] else 0.0
                ytd_user_value = row['ytd_user_value'] if row['ytd_user_value'] else 0.0

                sale_partner_id = row.get('sale_partner_id')

                partner_name = ''
                if sale_partner_id:
                    if self.env['sale.order'].sudo().search([('id', '=', sale_partner_id)]).partner_id.is_distributor == True:
                        partner_name = ''
                    else:
                        partner_name = self.env['sale.order'].sudo().search([('id', '=', sale_partner_id)]).partner_id.name

                user_units = row['user_units'] if row['user_units'] else 0.0
                user_value = row['user_value'] if row['user_value'] else 0.0
                user_collection = row['user_collection'] if row['user_collection'] else 0.0

                ftd_units = row['ftd_unit'] if row['ftd_unit'] else 0.0
                ftd_value = row['ftd_value'] if row['ftd_value'] else 0.0
                ftd_collection = row['ftd_collection'] if row['ftd_collection'] else 0.0

                mtd_value = row['mtd_value'] if row['mtd_value'] else 0.0
                mtd_units = row['mtd_unit'] if row['mtd_unit'] else 0.0

                mtd_dispatch_units = row['mtd_dispatch_units'] if row['mtd_dispatch_units'] else 0.0
                mtd_dispatch_value = row['mtd_dispatch_value'] if row['mtd_dispatch_value'] else 0.0

                area_of_user=''
                regional_manger_user = 0
                distributor = ''
                # if user_area != '':
                #     area_of_user = self.env['location.area'].sudo().search([('id', '=', user_area)]).name
                if user_name != ' ':
                    name_of_user = self.env['res.users'].sudo().search([('id', '=', user_name)]).name
                    units_of_user = self.env['res.users'].sudo().search([('id', '=', user_name)]).unit
                    value_of_user = self.env['res.users'].sudo().search([('id', '=', user_name)]).value
                    collection_of_user = self.env['res.users'].sudo().search([('id', '=', user_name)]).collection
                    if self.env['res.users'].sudo().search([('id', '=', user_name)]).partner_id:
                        if self.env['res.users'].sudo().search([('id', '=', user_name)]).partner_id.is_distributor==True:
                            distributor =''
                    #     if self.env['res.users'].sudo().search([('id', '=', user_name)]).partner_id.is_distributor==True:
                    #         distributor = ''
                        else:
                            # distributor = distributor
                            if self.env['res.partner'].sudo().search([('user_id', '=', user_name)]):
                                for partner_main in self.env['res.partner'].sudo().search([('user_id', '=', user_name)]):
                                    distributor = partner_main.name
                            else:
                                distributor = ''

                    if self.env['res.users'].sudo().search([('id', '=', user_name)]).area_id:
                        sample_area = self.env['res.users'].sudo().search([('id', '=', user_name)]).area_id

                        area_of_user = self.env['res.users'].sudo().search([('id', '=', user_name)]).area_id.name
                        if self.env['res.users'].sudo().search(
                            [('id', '=', user_name)]).area_id.state.regional_manager.id:
                            regional_manger_user = self.env['res.users'].sudo().search(
                            [('id', '=', user_name)]).area_id.state.regional_manager.id
                        if sample_area.area_manager:
                            area_manager_user = self.env['res.users'].sudo().search([('id', '=', user_name)]).area_id.area_manager.id
                        if sample_area.state_manager:
                            state_manager_user = self.env['res.users'].sudo().search([('id', '=', user_name)]).area_id.state_manager.id
                        if sample_area.state:
                            head_of_user = self.env['res.users'].sudo().search([('id', '=', user_name)]).area_id.state.head.id
                        else:
                            head_of_user =0
                            area_manager_user = 0
                            state_manager_user = 0
                            regional_manger_user = 0
                    else:
                        area_manager_user = 0
                        state_manager_user = 0
                        head_of_user = 0
                else:
                    name_of_user =""
                    area_of_user = ""
                    units_of_user = 0.0
                    value_of_user = 0.0
                    collection_of_user = 0.0
                    regional_manger_user = 0
                    area_manager_user = 0
                    state_manager_user = 0
                    head_of_user =0
                    # distributor = ''


                res = {
                    'sl_no': sl,
                    'name': name_of_user,
                    'area': area_of_user,
                    'distributor': distributor if distributor else "",
                    # 'distributor': partner_name if partner_name else "",
                    # 'user_units':units_of_user,
                    # 'user_value':  value_of_user,
                    # 'user_collection': collection_of_user,
                    'user_units':user_units,
                    'user_value':  user_value,
                    'user_collection': user_collection,
                    'ftd_units': ftd_units if ftd_units else 0.0,
                    'ftd_value': ftd_value if ftd_value else 0.0,
                    'ftd_collection': ftd_collection if ftd_collection else 0.0,
                    'mtd_value': mtd_value if mtd_value else 0.0,
                    'mtd_units': mtd_units if mtd_units else 0.0,
                    'mtd_dispatch_units': mtd_dispatch_units,
                    'mtd_dispatch_value': mtd_dispatch_value,
                    'regional_manager':  regional_manger_user,
                    'area_manager':  area_manager_user,
                    'state_manager': state_manager_user,
                    'head': head_of_user,
                    'mtd_dispatch_collection': mtd_dispatch_collection,
                    'carry_forward_value': carry_forward_value,
                    'carry_forward_unit': carry_forward_unit,
                    'ytd_target':ytd_target,
                    'ytd_user_value':ytd_user_value
                    # 'nrv': nrv

                }

                lines.append(res)

            area_manage = self.set_group_by_area_manager(lines)
            state_manage = self.set_group_by_state_manager(lines)
            regional_manage = self.set_group_by_regional_manager(lines)
            sl=0

            if '0.0' in regional_manage:
                del regional_manage['0.0']
            if 'false' in regional_manage:
                del regional_manage['false']
            regional_user_units = regional_user_value = regional_user_collection = regional_ftd_units = regional_ftd_value = regional_ftd_collection = regional_mtd_units \
                = regional_mtd_value = regional_mtd_per = regional_carry_forward_unit = regional_carry_forward_value = 0
            regional_mtd_dispatch_units = regional_mtd_dispatch_units_per = regional_mtd_dispatch_value = regional_mtd_dispatch_value_per = regional_nrv = regional_collection = regional_per = 0
            for regional_key, regional_value in regional_manage.items():
                regional_managers = self.env['res.users'].sudo().search([('id', '=', int(regional_key))]) if regional_key else 0

                regional_target_unit = regional_target_value = regional_target_collection = \
                    regional_ytd_target_collection = regional_ytd_target_achivement = 0

                regional_of_month = []
                regional_of_year = []
                ytd_target_list = []
                for months in range(date_from.month, (date_to.month + 1)):
                    regional_of_month.append(months)

                for years in range(date_from.year, (date_to.year + 1)):
                    regional_of_year.append(years)
                if regional_managers:
                    if regional_managers.sale_month_id:
                        regional_target = regional_managers.sale_month_id
                        user_regional_target = regional_target.sudo().search([('name', 'in', list(map(str, regional_of_month))), (
                        'year', 'in', list(map(str, regional_of_year))),('user_id','=',int(regional_key))]) if regional_target else 0
                        for i in user_regional_target:
                            regional_target_unit += i.unit
                            regional_target_value += i.value
                            regional_target_collection += i.collection
                        get_year_values = self._financial_year_values()

                        user_ytd_target = regional_target.sudo().search(
                            [('name', 'in', list(map(str, get_year_values[3]))), (
                                'year', 'in', list(map(str, get_year_values[2]))),('user_id','=',int(regional_key))]) if regional_target else 0
                        for i in user_ytd_target:
                            regional_ytd_target_collection += i.value

                regional_value =list(set(regional_value))
                for state in regional_value:
                    state_target_unit = state_target_value = state_target_collection \
                        = state_ytd_target_collection = state_ytd_target_achivement = 0
                    state_managers = self.env['res.users'].sudo().search([('id', '=', int(state))]) if state else 0

                    state_of_month = []
                    state_of_year = []
                    for months in range(date_from.month, (date_to.month + 1)):
                        state_of_month.append(months)
                        # list_of_month = map(str, list_of_month)

                    for years in range(date_from.year, (date_to.year + 1)):
                        state_of_year.append(years)
                    if state_managers:
                        if regional_managers.sale_month_id:
                            state_target = state_managers.sale_month_id
                            user_state_target = state_target.sudo().search([('name','in',list(map(str, state_of_month)))
                                                                               ,('year','in',list(map(str, state_of_year))),('user_id','=',int(state))]) if state_target else 0
                            for i in user_state_target:
                                state_target_unit +=i.unit
                                state_target_value +=i.value
                                state_target_collection +=i.collection
                            get_year_values = self._financial_year_values()

                            state_ytd_target = state_target.sudo().search(
                                [('name', 'in', list(map(str, get_year_values[3]))), (
                                    'year', 'in', list(map(str, get_year_values[2]))),('user_id','=',int(state))]) if regional_target else 0
                            for i in state_ytd_target:
                                state_ytd_target_collection += i.value

                    state_user_units = state_user_value = state_user_collection \
                        = state_ftd_units = state_ftd_value = state_ftd_collection = state_mtd_units \
                        = state_carry_forward_unit = state_carry_forward_value \
                        = state_mtd_value = state_mtd_per = 0
                    state_mtd_dispatch_units = state_mtd_dispatch_units_per\
                        = state_mtd_dispatch_value = state_mtd_dispatch_value_per \
                        = state_nrv = state_collection = state_per = 0

                    state_manage[str(state)] = list(set(state_manage[str(state)]))

                    # sl += 1
                    for area in state_manage[str(state)]:
                        area_managers = self.env['res.users'].sudo().search([('id', '=', int(area))]) if area else 0

                        area_user_units = area_user_value = area_user_collection = area_ftd_units = area_ftd_value \
                            = area_carry_forward_unit = area_carry_forward_value = area_ftd_collection\
                            = area_mtd_units = area_mtd_value = area_mtd_per = 0
                        area_mtd_dispatch_units = area_mtd_dispatch_units_per = area_mtd_dispatch_value \
                            = area_mtd_dispatch_value_per = area_nrv = area_collection \
                            = area_per = area_ytd_target_collection = area_ytd_target_achivement = 0

                        for each in area_manage[str(area)]:
                            sl += 1

                            worksheet.write(prod_row, prod_col,sl, style)

                            worksheet.write(prod_row, prod_col + 1, each['name'] if each['name'] else '', style1)

                            worksheet.write(prod_row, prod_col + 2, each['area'], style1)

                            worksheet.write(prod_row, prod_col + 3, each['distributor'], style1)

                            worksheet.write(prod_row, prod_col + 4, each['carry_forward_unit'], style1)
                            area_carry_forward_unit += each['carry_forward_unit']

                            worksheet.write(prod_row, prod_col + 5, each['carry_forward_value'], style1)
                            area_carry_forward_value += each['carry_forward_value']

                            worksheet.write(prod_row, prod_col + 6, float('%.2f' %(each['user_units'])), style)
                            area_user_units+=each['user_units']

                            worksheet.write(prod_row, prod_col + 7, float('%.2f' %(each['user_value'])), style)
                            area_user_value += each['user_value']

                            worksheet.write(prod_row, prod_col + 8,  float('%.2f' %(each['user_collection'])), style)
                            area_user_collection += each['user_collection']

                            worksheet.write(prod_row, prod_col + 9,  float('%.2f' %(each['ftd_units'])), style)
                            area_ftd_units += each['ftd_units']

                            worksheet.write(prod_row, prod_col + 10,  float('%.2f' %(each['ftd_value'])), style)
                            area_ftd_value += each['ftd_value']

                            worksheet.write(prod_row, prod_col + 11,  float('%.2f' %(each['ftd_collection'])), style)
                            area_ftd_collection += each['ftd_collection']

                            worksheet.write(prod_row, prod_col + 12,  float('%.2f' %(each['mtd_units'])), style)
                            area_mtd_units += each['mtd_units']

                            worksheet.write(prod_row, prod_col + 13,  float('%.2f' %(each['mtd_value'])), style)
                            area_mtd_value += each['mtd_value']

                            worksheet.write(prod_row, prod_col + 14,  float('%.2f' %((each['mtd_value']/each['user_value'])*100)) if each['user_value'] !=0 else 0.00, style)
                            area_mtd_per += ((each['mtd_value']/each['user_value'])*100  if each['user_value'] !=0 else 0.00)

                            worksheet.write(prod_row, prod_col + 15,  float('%.2f' %(each['mtd_dispatch_units'])), style)
                            area_mtd_dispatch_units += each['mtd_dispatch_units']

                            worksheet.write(prod_row, prod_col + 16,  float('%.2f' %((each['mtd_dispatch_units']/each['user_units'])*100)) if each['user_units'] !=0 else 0.00, style)
                            area_mtd_dispatch_units_per += ((each['mtd_dispatch_units']/each['user_units'])*100 if each['user_units'] !=0 else 0.00)
                            worksheet.write(prod_row, prod_col + 17,  float('%.2f' %(each['mtd_dispatch_value'])), style)
                            area_mtd_dispatch_value += each['mtd_dispatch_value']

                            worksheet.write(prod_row, prod_col + 18,   float('%.2f' %((each['mtd_dispatch_value']/each['user_value'])*100)) if each['user_value'] !=0 else 0.00, style)
                            area_mtd_dispatch_value_per +=((each['mtd_dispatch_value']/each['user_value'])*100 if each['user_value'] !=0 else 0.00)

                            worksheet.write(prod_row, prod_col + 19,  float('%.2f' %((each['mtd_dispatch_value']/each['mtd_dispatch_units']))) if each['mtd_dispatch_units'] !=0 else 0.00, style)
                            area_nrv += ((each['mtd_dispatch_value']/each['mtd_dispatch_units']) if each['mtd_dispatch_units'] !=0 else 0.00)
                            worksheet.write(prod_row, prod_col + 20,  float('%.2f' %(each['mtd_dispatch_collection'])), style)
                            area_collection += each['mtd_dispatch_collection']
                            worksheet.write(prod_row, prod_col + 21,  float('%.2f' %((each['mtd_dispatch_collection']/each['user_collection'])*100)) if each['user_collection'] !=0 else 0.00, style)

                            worksheet.write(prod_row, prod_col + 22,  float('%.2f' %((each['ytd_target']))), style)
                            area_ytd_target_collection += each['ytd_target']


                            worksheet.write(prod_row, prod_col + 23,  float('%.2f' %((each['ytd_user_value']))), style)
                            area_ytd_target_achivement+=each['ytd_user_value']

                            prod_row = prod_row + 1
                            line_column = 0
                        sl+=1
                        worksheet.write(prod_row, prod_col, sl, format1)

                        worksheet.write(prod_row, prod_col + 1, area_managers.name if area_managers else '', format11)

                        worksheet.write(prod_row, prod_col + 2, "", format1)

                        worksheet.write(prod_row, prod_col + 3, "", format1)

                        worksheet.write(prod_row, prod_col + 4, float('%.2f' % area_carry_forward_unit), format1)
                        state_carry_forward_unit += area_carry_forward_unit

                        worksheet.write(prod_row, prod_col + 5, float('%.2f' % area_carry_forward_value), format1)
                        state_carry_forward_value += area_carry_forward_value

                        worksheet.write(prod_row, prod_col + 6,  float('%.2f' %area_user_units), format1)
                        state_user_units += area_user_units

                        worksheet.write(prod_row, prod_col + 7,  float('%.2f' %area_user_value), format1)
                        state_user_value += area_user_value

                        worksheet.write(prod_row, prod_col + 8,  float('%.2f' %area_user_collection), format1)
                        state_user_collection += area_user_collection

                        worksheet.write(prod_row, prod_col + 9,  float('%.2f' %area_ftd_units), format1)
                        state_ftd_units += area_ftd_units

                        worksheet.write(prod_row, prod_col + 10,  float('%.2f' %area_ftd_value), format1)
                        state_ftd_value += area_ftd_value

                        worksheet.write(prod_row, prod_col + 11,  float('%.2f' %area_ftd_collection), format1)
                        state_ftd_collection += area_ftd_collection

                        worksheet.write(prod_row, prod_col + 12,  float('%.2f' %area_mtd_units),format1)
                        state_mtd_units += area_mtd_units

                        worksheet.write(prod_row, prod_col + 13,  float('%.2f' %area_mtd_value),format1)
                        state_mtd_value += area_mtd_value

                        # worksheet.write(prod_row, prod_col + 12,  float('%.2f' %area_mtd_per), format1)
                        worksheet.write(prod_row, prod_col + 14, float('%.2f' %((area_mtd_value/area_user_value)*100)) if area_user_value !=0 else 0.00, format1)
                        state_mtd_per += area_mtd_per

                        worksheet.write(prod_row, prod_col + 15,  float('%.2f' %area_mtd_dispatch_units), format1)
                        state_mtd_dispatch_units += area_mtd_dispatch_units

                        # worksheet.write(prod_row, prod_col + 14, float('%.2f' %area_mtd_dispatch_units_per), format1)
                        worksheet.write(prod_row, prod_col + 16, float('%.2f' %((area_mtd_dispatch_units/area_user_units)*100)) if area_user_units !=0 else 0.00, format1)
                        state_mtd_dispatch_units_per += area_mtd_dispatch_units_per
                        worksheet.write(prod_row, prod_col + 17,  float('%.2f' %area_mtd_dispatch_value), format1)
                        state_mtd_dispatch_value += area_mtd_dispatch_value

                        # worksheet.write(prod_row, prod_col + 16,  float('%.2f' %area_mtd_dispatch_value_per),format1)
                        worksheet.write(prod_row, prod_col + 18,  float('%.2f' %((area_mtd_dispatch_value/area_user_value)*100)) if area_user_value !=0 else 0.00,format1)
                        state_mtd_dispatch_value_per += area_mtd_dispatch_value_per

                        # worksheet.write(prod_row, prod_col + 17,  float('%.2f' %area_nrv), format1)
                        worksheet.write(prod_row, prod_col + 19,  float('%.2f' %((area_mtd_dispatch_value/area_mtd_dispatch_units))) if area_mtd_dispatch_units !=0 else 0.00, format1)
                        state_nrv += area_nrv
                        worksheet.write(prod_row, prod_col + 20,  float('%.2f' %area_collection), format1)
                        state_collection += area_collection
                        worksheet.write(prod_row, prod_col + 21,   float('%.2f' %((area_collection/area_user_collection)*100)) if area_user_collection !=0 else 0.00, format1)
                        state_per += area_per

                        worksheet.write(prod_row, prod_col + 22, float('%.2f' %area_ytd_target_collection),  format1)
                        # state_ytd_target_collection +=area_ytd_target_collection

                        worksheet.write(prod_row, prod_col + 23, float('%.2f' %area_ytd_target_achivement),  format1)
                        state_ytd_target_achivement +=area_ytd_target_achivement

                        prod_row = prod_row + 1
                        line_column = 0
                    sl += 1
                    worksheet.write(prod_row, prod_col, sl, format2)

                    worksheet.write(prod_row, prod_col + 1, state_managers.name if state_managers else '', format21)

                    worksheet.write(prod_row, prod_col + 2, "", format2)

                    worksheet.write(prod_row, prod_col + 3, "", format2)

                    worksheet.write(prod_row, prod_col + 4, float('%.2f' % state_carry_forward_unit), format2)
                    regional_carry_forward_unit += state_carry_forward_unit

                    worksheet.write(prod_row, prod_col + 5, float('%.2f' % state_carry_forward_value), format2)
                    regional_carry_forward_value += state_carry_forward_value

                    # worksheet.write(prod_row, prod_col + 4,  float('%.2f' %state_user_units), format2)
                    worksheet.write(prod_row, prod_col + 6,  float('%.2f' %state_target_unit), format2)
                    regional_user_units += state_user_units

                    # worksheet.write(prod_row, prod_col + 5,  float('%.2f' %state_user_value), format2)
                    worksheet.write(prod_row, prod_col + 7,  float('%.2f' %state_target_value), format2)
                    regional_user_value += state_user_value

                    # worksheet.write(prod_row, prod_col + 6,  float('%.2f' %state_user_collection), format2)
                    worksheet.write(prod_row, prod_col + 8,  float('%.2f' %state_target_collection), format2)
                    regional_user_collection += state_user_collection

                    worksheet.write(prod_row, prod_col + 9,  float('%.2f' %state_ftd_units), format2)
                    regional_ftd_units += state_ftd_units

                    worksheet.write(prod_row, prod_col + 10,  float('%.2f' %state_ftd_value), format2)
                    regional_ftd_value += state_ftd_value

                    worksheet.write(prod_row, prod_col + 11,  float('%.2f' %state_ftd_collection), format2)
                    regional_ftd_collection += state_ftd_collection

                    worksheet.write(prod_row, prod_col + 12,  float('%.2f' %state_mtd_units), format2)
                    regional_mtd_units += state_mtd_units

                    worksheet.write(prod_row, prod_col + 13,  float('%.2f' %state_mtd_value), format2)
                    regional_mtd_value += state_mtd_value

                    # worksheet.write(prod_row, prod_col + 12,  float('%.2f' %state_mtd_per), format2)
                    worksheet.write(prod_row, prod_col + 14,  float('%.2f' %((state_mtd_value/state_user_value)*100)) if state_user_value !=0 else 0.00, format2)
                    regional_mtd_per += state_mtd_per

                    worksheet.write(prod_row, prod_col + 15,  float('%.2f' %state_mtd_dispatch_units), format2)
                    regional_mtd_dispatch_units += state_mtd_dispatch_units

                    # worksheet.write(prod_row, prod_col + 14,  float('%.2f' %state_mtd_dispatch_units_per), format2)
                    worksheet.write(prod_row, prod_col + 16, float('%.2f' %((state_mtd_dispatch_units/state_user_units)*100)) if state_user_units !=0 else 0.00, format2)
                    regional_mtd_dispatch_units_per += state_mtd_dispatch_units_per
                    worksheet.write(prod_row, prod_col + 17,  float('%.2f' %state_mtd_dispatch_value), format2)
                    regional_mtd_dispatch_value += state_mtd_dispatch_value

                    # worksheet.write(prod_row, prod_col + 16,  float('%.2f' %state_mtd_dispatch_value_per), format2)
                    worksheet.write(prod_row, prod_col + 18,  float('%.2f' %((state_mtd_dispatch_value/state_user_value)*100)) if state_user_value !=0 else 0.00, format2)
                    regional_mtd_dispatch_value_per += state_mtd_dispatch_value_per

                    # worksheet.write(prod_row, prod_col + 17,  float('%.2f' %state_nrv), format2)
                    worksheet.write(prod_row, prod_col + 19,  float('%.2f' %((state_mtd_dispatch_value/state_mtd_dispatch_units))) if state_mtd_dispatch_units !=0 else 0.00, format2)
                    regional_nrv += state_nrv
                    worksheet.write(prod_row, prod_col + 20,  float('%.2f' %state_collection), format2)
                    regional_collection += state_collection
                    # worksheet.write(prod_row, prod_col + 19, float('%.2f' %state_per), format2)
                    worksheet.write(prod_row, prod_col + 21, float('%.2f' %((state_collection/state_user_collection)*100)) if state_user_collection !=0 else 0.00, format2)
                    regional_per += state_per

                    worksheet.write(prod_row, prod_col + 22,float('%.2f' %state_ytd_target_collection), format2)
                    # regional_ytd_target_collection += state_ytd_target_collection

                    worksheet.write(prod_row, prod_col + 23, state_ytd_target_achivement, format2)
                    regional_ytd_target_achivement += state_ytd_target_achivement


                    prod_row = prod_row + 1
                    line_column = 0
                sl += 1
                worksheet.write(prod_row, prod_col, sl, format3)

                worksheet.write(prod_row, prod_col + 1, regional_managers.name if regional_managers else '', format31)

                worksheet.write(prod_row, prod_col + 2, "", format3)

                worksheet.write(prod_row, prod_col + 3, "", format3)

                worksheet.write(prod_row, prod_col + 4, float('%.2f' % regional_carry_forward_unit), format3)

                worksheet.write(prod_row, prod_col + 5, float('%.2f' % regional_carry_forward_value), format3)

                # worksheet.write(prod_row, prod_col + 4,  float('%.2f' % regional_user_units), format3)
                worksheet.write(prod_row, prod_col + 6,  float('%.2f' % regional_target_unit), format3)

                # worksheet.write(prod_row, prod_col + 5, float('%.2f' % regional_user_value), format3)
                worksheet.write(prod_row, prod_col + 7, float('%.2f' % regional_target_value), format3)

                # worksheet.write(prod_row, prod_col + 6, float('%.2f' % regional_user_collection), format3)
                worksheet.write(prod_row, prod_col + 8, float('%.2f' % regional_target_collection), format3)

                worksheet.write(prod_row, prod_col + 9, float('%.2f' % regional_ftd_units),format3)

                worksheet.write(prod_row, prod_col + 10, float('%.2f' % regional_ftd_value), format3)

                worksheet.write(prod_row, prod_col + 11, float('%.2f' % regional_ftd_collection),format3)

                worksheet.write(prod_row, prod_col + 12, float('%.2f' % regional_mtd_units), format3)

                worksheet.write(prod_row, prod_col + 13, float('%.2f' % regional_mtd_value),format3)

                # worksheet.write(prod_row, prod_col + 12, float('%.2f' % regional_mtd_per),format3)
                worksheet.write(prod_row, prod_col + 14, float('%.2f' %((regional_mtd_value/regional_user_value)*100)) if regional_user_value !=0 else 0.00,format3)

                worksheet.write(prod_row, prod_col + 15,  float('%.2f' % regional_mtd_dispatch_units), format3)

                # worksheet.write(prod_row, prod_col + 14, float('%.2f' % regional_mtd_dispatch_units_per), format3)
                worksheet.write(prod_row, prod_col + 16, float('%.2f' %((regional_mtd_dispatch_units/regional_user_units)*100)) if regional_user_units !=0 else 0.00, format3)
                worksheet.write(prod_row, prod_col + 17, float('%.2f' % regional_mtd_dispatch_value),format3)

                # worksheet.write(prod_row, prod_col + 16, float('%.2f' % regional_mtd_dispatch_value_per), format3)
                worksheet.write(prod_row, prod_col + 18, float('%.2f' %((regional_mtd_dispatch_value/regional_user_value)*100)) if regional_user_value !=0 else 0.00, format3)

                # worksheet.write(prod_row, prod_col + 17, float('%.2f' % regional_nrv),format3)
                worksheet.write(prod_row, prod_col + 19,  float('%.2f' %((regional_mtd_dispatch_value/regional_mtd_dispatch_units))) if regional_mtd_dispatch_units !=0 else 0.00,format3)
                worksheet.write(prod_row, prod_col + 20, float('%.2f' % regional_collection), format3)
                # worksheet.write(prod_row, prod_col + 19, float('%.2f' % regional_per), format3)
                worksheet.write(prod_row, prod_col + 21,  float('%.2f' %((regional_collection/regional_user_collection)*100)) if regional_user_collection !=0 else 0.00, format3)

                worksheet.write(prod_row, prod_col + 22,  float('%.2f' %regional_ytd_target_collection), format3)

                worksheet.write(prod_row, prod_col + 23,  float('%.2f' %regional_ytd_target_achivement), format3)

                prod_row = prod_row + 1
                line_column = 0



            # worksheet.write_merge(prod_row, 0, prod_row, 2, "TOTAL", style)
            #
            # # total_cell_range2 = xl_range(8, 2, prod_row - 1, 2)
            # total_cell_range3 = xl_range(6, 3, prod_row - 1, 3)
            # total_cell_range = xl_range(6, 4, prod_row - 1, 4)
            # total_cell_range11 = xl_range(6, 5, prod_row - 1, 5)
            # total_cell_range6 = xl_range(6, 6, prod_row - 1, 6)
            # total_cell_range7 = xl_range(6, 7, prod_row - 1, 7)
            # total_cell_range8 = xl_range(6, 8, prod_row - 1, 8)
            # total_cell_range9 = xl_range(6, 9, prod_row - 1, 9)
            # total_cell_range10 = xl_range(6, 10, prod_row - 1, 10)
            #
            # # sheet.write_formula(prod_row, 2, '=SUM(' + total_cell_range2 + ')', style)
            # worksheet.write_formula(prod_row, 3, '=SUM(' + total_cell_range3 + ')', style)
            # worksheet.write_formula(prod_row, 4, '=SUM(' + total_cell_range + ')', style)
            # worksheet.write_formula(prod_row, 5, '=SUM(' + total_cell_range11 + ')', style)
            # worksheet.write_formula(prod_row, 6, '=SUM(' + total_cell_range6 + ')', style)
            # worksheet.write_formula(prod_row, 7, '=SUM(' + total_cell_range7 + ')', style)
            # worksheet.write_formula(prod_row, 8, '=SUM(' + total_cell_range8 + ')', style)
            # worksheet.write_formula(prod_row, 9, '=SUM(' + total_cell_range9 + ')', style)
            # worksheet.write_formula(prod_row, 10, '=SUM(' + total_cell_range10 + ')', style)

            prod_row = 8

            prod_col = 7

            fp = io.BytesIO()

            workbook.save(fp)

            export_id = self.env['sale.report.excel'].create(

                {'excel_file': base64.encodestring(fp.getvalue()), 'file_name': filename})

            res = {

                'view_mode': 'form',

                'res_id': export_id.id,

                'res_model': 'sale.report.excel',

                'type': 'ir.actions.act_window',

                'target': 'new'

            }

            return res

        else:
            raise Warning(
                """ You Don't have xlwt library.\n Please install it by executing this command :  sudo pip3 install xlwt""")


class Sale_Report_excel(models.TransientModel):
    _name = "sale.report.excel"
    _description = "DSR Report Excel"

    excel_file = fields.Binary('Excel Report For DSR report ')
    file_name = fields.Char('Excel File', size=64)


