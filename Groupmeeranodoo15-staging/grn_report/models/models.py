# -*- coding: utf-8 -*-

from odoo import models, fields, api

import base64
from odoo import api, fields, models
from odoo.exceptions import Warning
import io
import datetime
from datetime import datetime

try:
    import xlwt
except ImportError:
    xlwt = None


class grn_report_wizard(models.TransientModel):
    _name = "grn.report.wizard"
    _description = "GRN Report Wizard"

    start_date = fields.Date('Start Period', required=True)
    end_date = fields.Date('End Period', required=True)
    company_id = fields.Many2one('res.company', string='Company',required=True)
    vendor_id = fields.Many2one('res.partner', string='Vendor')

    def get_company(self):

        if self.company_id:
            l1 = []
            l2 = []
            obj = self.env['res.company'].search([('id', '=', self.company_id.id)])
            l1.append(obj.name)
            return l1

    def get_report_date(self, data):
        date_from = self.start_date
        date_to = self.end_date
        vendor_id = self.vendor_id.id
        product_res = self.env['product.product'].search([('qty_available', '!=', 0), ('type', '=', 'product'), ])
        category_lst = [0]
        product_lst = [0]
        warehouse_lst = [0]
        loc_list = [0]

        locations = [0]

        lines = []
        final_result = []
        sl = 0

        if data['vendor_id']:

            query = '''       
                  	select 
			    sum(m.product_uom_qty) as received_qty,
               	max(p.origin) as origin,
                max(p.name) as name,
				p.partner_id,
				max(po.price_unit) as cost,
				max(p.date_done) as effective_date,
				sum(po.product_qty) as demanded_qty,
				sum(m.product_uom_qty*po.price_unit) as unit_price,
               m.product_id
          from stock_move as m 
                   left join stock_picking as p on p.id= m.picking_id 
                   left join stock_picking_type spt on spt.id=p.picking_type_id
		 		   left join purchase_order_line as po on m.purchase_line_id=po.id
                   where 
                   spt.code='incoming' 
                   and to_char(date_trunc('day',p.date_done),'YYYY-MM-DD')::date between %s and %s
                   and p.partner_id = %s
                    and m.state in ('done')
                      group by to_char(date_trunc('day',m.date),'YYYY-MM-DD'),m.product_id,p.partner_id
               '''
            self.env.cr.execute(query, (
                date_from, date_to,vendor_id
            ))
            for row in self.env.cr.dictfetchall():
                sl += 1
                demanded_qty = row.get('demanded_qty') if row.get('demanded_qty') else 0.0
                effective_dates = row.get('effective_date') if row.get('effective_date') else ''
                if effective_dates:
                    effective_date = datetime.strptime(str(effective_dates), '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y')
                else:
                    effective_date = ''
                received_qty = row.get('received_qty') if row.get('received_qty') else 0.0
                origin = row.get('origin') if row.get('origin') else ''
                name = row.get('name') if row.get('name') else " "
                unit_price = row.get('unit_price') if row.get('unit_price') else 0
                product_id = row.get('product_id') if row.get('product_id') else 0
                partner_id = row.get('partner_id') if row.get('partner_id') else 0
                cost = row.get('cost') if row.get('cost') else 0
                product = self.env['product.product'].search([('id', '=', int(product_id))])
                partner = self.env['res.partner'].search([('id', '=', int(partner_id))])

                res = {
                    'sl_no': sl,
                    'productname': product.name or '',
                    'demanded_qty': demanded_qty or 0,
                    'origin': origin,
                    'name': name or '',
                    'partner': partner.name or '',
                    'cost': cost or 0,
                    'received_qty':received_qty,
                    'effective_date':effective_date,
                    'unit_price':unit_price

                }

                lines.append(res)
            return lines
        else:


            query = '''       
                            select 
                        sum(m.product_uom_qty) as received_qty,
                        max(p.origin) as origin,
                        max(p.name) as name,
                        p.partner_id,
                        max(po.price_unit) as cost,
                        max(p.date_done) as effective_date,
                        sum(po.product_qty) as demanded_qty,
                        sum(m.product_uom_qty*po.price_unit) as unit_price,
                       m.product_id
                  from stock_move as m 
                           left join stock_picking as p on p.id= m.picking_id 
                           left join stock_picking_type spt on spt.id=p.picking_type_id
                           left join purchase_order_line as po on m.purchase_line_id=po.id
                           where 
                           spt.code='incoming' 
                           and to_char(date_trunc('day',p.date_done),'YYYY-MM-DD')::date between %s and %s
                            and m.state in ('done')
                              group by to_char(date_trunc('day',m.date),'YYYY-MM-DD'),m.product_id,p.partner_id
                       '''
            self.env.cr.execute(query, (
                date_from, date_to
            ))
            for row in self.env.cr.dictfetchall():
                sl += 1
                demanded_qty = row.get('demanded_qty') if row.get('demanded_qty') else 0.0
                effective_dates = row.get('effective_date') if row.get('effective_date') else ''
                if effective_dates:
                    effective_date = datetime.strptime(str(effective_dates), '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y')
                else:
                    effective_date = ''
                received_qty = row.get('received_qty') if row.get('received_qty') else 0.0
                origin = row.get('origin') if row.get('origin') else ''
                name = row.get('name') if row.get('name') else " "
                unit_price = row.get('unit_price') if row.get('unit_price') else 0
                product_id = row.get('product_id') if row.get('product_id') else 0
                partner_id = row.get('partner_id') if row.get('partner_id') else 0
                cost = row.get('cost') if row.get('cost') else 0
                product = self.env['product.product'].search([('id', '=', int(product_id))])
                partner = self.env['res.partner'].search([('id', '=', int(partner_id))])

                res = {
                    'sl_no': sl,
                    'productname': product.name or '',
                    'demanded_qty': demanded_qty or 0,
                    'origin': origin,
                    'name': name or '',
                    'partner': partner.name or '',
                    'cost': cost or 0,
                    'received_qty': received_qty,
                    'effective_date': effective_date,
                    'unit_price': unit_price

                }

                lines.append(res)
        return lines



    def print_exl_report(self):
        if xlwt:
            data = {
                'start_date': self.start_date,
                'end_date': self.end_date,
                'company_id': self.company_id.name,
                'vendor_id': self.vendor_id.id,
            }
            filename = 'GRN Report.xls'
            l1 = []
            get_company = self.get_company()
            workbook = xlwt.Workbook()
            stylePC = xlwt.XFStyle()
            alignment = xlwt.Alignment()
            alignment.horz = xlwt.Alignment.HORZ_CENTER
            fontP = xlwt.Font()
            fontP.bold = True
            fontP.height = 200
            stylePC.font = fontP
            stylePC.num_format_str = '@'
            stylePC.alignment = alignment
            style_title = xlwt.easyxf(
                "font:height 300; font: name Liberation Sans, bold on,color blue; align: horiz center")
            style_table_header = xlwt.easyxf(
                "font:height 200; font: name Liberation Sans, bold on,color black; align: horiz center")
            style = xlwt.easyxf("font:height 200; font: name Liberation Sans,color black;")
            style1 = xlwt.easyxf("font:height 200; font: name Liberation Sans,color black;align: horiz center")
            worksheet = workbook.add_sheet('Sheet 1')
            worksheet.write(5, 1, 'Start Date:', style_table_header)
            worksheet.write(6, 1, str(self.start_date))
            worksheet.write(5, 2, 'End Date', style_table_header)
            worksheet.write(6, 2, str(self.end_date))
            worksheet.write(5, 3, 'Company', style_table_header)
            worksheet.write(6, 3, get_company and get_company[0] or '', )


            w_col_no = 7
            w_col_no1 = 8

            worksheet.write_merge(0, 1, 1, 9, "GRN Report", style=style_title)
            worksheet.write(8, 0, 'Sl No', style_table_header)
            worksheet.write(8, 1, 'PO Number', style_table_header)
            worksheet.write(8, 2, 'Reference', style_table_header)
            worksheet.write(8, 3, 'Vendor', style_table_header)
            worksheet.write(8, 4, 'Received Date', style_table_header)
            worksheet.write(8, 5, 'Product', style_table_header)
            worksheet.write(8, 6, 'Demanded Qty', style_table_header)
            worksheet.write(8, 7, 'Cost', style_table_header)
            worksheet.write(8, 8, 'Received Qty', style_table_header)
            worksheet.write(8, 9, 'Unit Price', style_table_header)

            prod_row = 9
            prod_col = 0

            get_line = self.get_report_date(data)
            s = 0

            s = 0

            for each in get_line:
                worksheet.write(prod_row, prod_col, s + 1, style1)
                worksheet.write(prod_row, prod_col + 1, each['origin'], style)
                worksheet.write(prod_row, prod_col + 2, each['name'], style)
                worksheet.write(prod_row, prod_col + 3, (each['partner']), style)
                worksheet.write(prod_row, prod_col + 4, (each['effective_date']), style)
                worksheet.write(prod_row, prod_col + 5, (each['productname']), style)
                worksheet.write(prod_row, prod_col + 6, (each['demanded_qty']), style)
                worksheet.write(prod_row, prod_col + 7, (each['cost']), style)
                worksheet.write(prod_row, prod_col + 8, (each['received_qty']), style)
                worksheet.write(prod_row, prod_col + 9, (each['unit_price']), style)
                prod_row = prod_row + 1
                s += 1


            prod_row = 10
            prod_col = 7

            fp = io.BytesIO()
            workbook.save(fp)

            export_id = self.env['grn.report.excel'].create(
                {'excel_file': base64.encodebytes(fp.getvalue()), 'file_name': filename})
            res = {
                'view_mode': 'form',
                'res_id': export_id.id,
                'res_model': 'grn.report.excel',
                'type': 'ir.actions.act_window',
                'target': 'new'
            }
            return res
        else:
            raise Warning(
                """ You Don't have xlwt library.\n Please install it by executing this command :  sudo pip3 install xlwt""")


class grn_report_excel(models.TransientModel):
    _name = "grn.report.excel"
    _description = "GRN Report Excel"

    excel_file = fields.Binary('Excel Report For GRN Report')
    file_name = fields.Char('Excel File', size=64)
