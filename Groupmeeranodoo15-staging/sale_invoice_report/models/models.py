# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta, date

import logging

_logger = logging.getLogger(__name__)

try:
    import xlsxwriter
except ImportError:
    _logger.debug('Cannot `import xlsxwriter`.')
try:
    import base64
except ImportError:
    _logger.debug('Cannot `import base64`.')


class SaleInvoiceReportWizard(models.TransientModel):
    _name = "sale.invoice.report.wizard"
    _description = "Sale Invoice Report Wizard"

    start_date = fields.Date('Start Date', required=True, default=date.today())
    end_date = fields.Date('End Date', required=True, default=date.today())
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    document = fields.Binary('File To Download')
    remove_freebies = fields.Boolean(string='Remove Freebies', default=True, required=True)
    file = fields.Char('Report File Name', readonly=1)

    def get_sale_details(self, data):
        lines = []
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        company = data.get('company_id')
        remove_freebies = data.get('remove_freebies')
        if remove_freebies:
            invoice_lines = self.env['account.move.line'].search([('move_id.invoice_date', '>=', start_date),
                                                                  ('move_id.invoice_date', '<=', end_date),
                                                                  ('company_id.id', '=', company.id),
                                                                  ('move_id.state', '=', 'posted'),
                                                                  ('move_id.move_type', '=', 'out_invoice'),
                                                                  ('display_type', '=', False),
                                                                  ('exclude_from_invoice_tab', '=', False),
                                                                  ('product_id.freebie', '!=', True)])
        else:
            invoice_lines = self.env['account.move.line'].search([('move_id.invoice_date', '>=', start_date),
                                                                  ('move_id.invoice_date', '<=', end_date),
                                                                  ('company_id.id', '=', company.id),
                                                                  ('move_id.state', '=', 'posted'),
                                                                  ('move_id.move_type', '=', 'out_invoice'),
                                                                  ('display_type', '=', False),
                                                                  ('exclude_from_invoice_tab', '=', False)])
        for line in invoice_lines:
            value = {}
            variant = ""
            if line.product_id.product_template_attribute_value_ids:
                variant = line.product_id.product_template_attribute_value_ids._get_combination_name()
                name = variant and "%s (%s)" % (line.product_id.name, variant) or line.product_id.name
                product_name = name
            else:
                product_name = line.product_id.name
            ordered_qty = [x.product_uom_qty for x in line.sale_line_ids] or [0]
            ordered_value = [y.price_subtotal for y in line.sale_line_ids] or [0]
            invoiced_qty = [z.qty_invoiced for z in line.sale_line_ids] or [0]
            value.update({
                'invoice_no': line.move_name,
                'invoice_date': datetime.strptime(str(line.move_id.invoice_date), "%Y-%m-%d").strftime("%d-%m-%Y"),
                'voucher_type': 'GST Sales',
                'party_name': line.move_id.partner_id.name,
                'item_code': line.product_id.default_code or '',
                'product_id': line.product_id.id,
                'item_name': line.product_id.name or '',
                'attribute_value': variant,
                'category': line.product_id.categ_id.name or '',
                'label_category': line.product_id.label_category.name or '',
                'sale_order_no': ', '.join(map(lambda x: x.order_id.name, line.sale_line_ids)) or "",
                'ordered_qty': sum(ordered_qty) or 0.00,
                'ordered_value': sum(ordered_value) or 0.00,
                'billed_qty': line.quantity or 0.0,
                'billed_value': line.price_subtotal or 0.0,
                'pending_qty': (sum(ordered_qty) - sum(invoiced_qty)) if sum(ordered_qty) >= sum(invoiced_qty) else 0.0,
                'pending_value': (sum(ordered_value) - line.price_subtotal)
                if sum(ordered_value) >= line.price_subtotal else 0.0,
                'discount_value': (line.quantity*line.price_unit)-line.price_subtotal,
                'area': line.move_id.invoice_user_id.area_id.name or "",
                'sales_person': line.move_id.invoice_user_id.name or "",
                'tag': ', '.join(map(lambda x: x.name, line.move_id.partner_id.category_id)) or "",
                'asm': line.move_id.invoice_user_id.area_id.area_manager.name or "",
                'warehouse': line.move_id.warehouse_id.name or "",
            })
            lines.append(value)

        return lines

    def print_excel_report(self):
        self.ensure_one()
        [data] = self.read()
        file_path = 'Base Report' + '.xlsx'
        workbook = xlsxwriter.Workbook('/tmp/' + file_path)
        worksheet = workbook.add_worksheet('Base Report')

        header_format = workbook.add_format(
            {'bold': True, 'valign': 'vcenter', 'font_size': 16, 'align': 'center', 'bg_color': '#D8D8D8'})
        title_format = workbook.add_format(
            {'border': 1, 'bold': True, 'valign': 'vcenter', 'align': 'center', 'font_size': 14, 'bg_color': '#D8D8D8'})
        cell_wrap_format = workbook.add_format(
            {'border': 1, 'valign': 'vjustify', 'valign': 'vcenter', 'align': 'left', 'font_size': 12, })  ##E6E6E6
        cell_wrap_format_right = workbook.add_format(
            {'border': 1, 'valign': 'vjustify', 'valign': 'vcenter', 'align': 'right', 'font_size': 12, })  ##E6E6E6
        cell_wrap_format_val = workbook.add_format(
            {'border': 1, 'valign': 'vjustify', 'valign': 'vcenter', 'align': 'right', 'font_size': 12, })  ##E6E6E6
        cell_wrap_format_val.set_font_color('#006600')
        cell_wrap_format_bold = workbook.add_format(
            {'border': 1, 'bold': True, 'valign': 'vjustify', 'valign': 'vcenter', 'align': 'center', 'font_size': 12,
             'bg_color': '#D8D8D8'})  ##E6E6E6
        cell_wrap_format_amount = workbook.add_format(
            {'border': 1, 'valign': 'vjustify', 'valign': 'vcenter', 'align': 'right', 'font_size': 12,
             'bold': True})  ##E6E6E6
        cell_wrap_format_amount_val = workbook.add_format(
            {'border': 1, 'valign': 'vjustify', 'valign': 'vcenter', 'align': 'right', 'font_size': 12,
             'bold': True})  ##E6E6E6
        cell_wrap_format_amount.set_font_color('#006600')

        worksheet.set_row(1, 20)  # Set row height
        # Merge Row Columns
        TITLEHEDER = 'Base Report'
        worksheet.set_column(0, 20, 20)

        start_date = data.get('start_date')
        end_date = data.get('end_date')
        start_date = datetime.strptime(str(start_date), "%Y-%m-%d").strftime("%Y-%m-%d")
        end_date = datetime.strptime(str(end_date), "%Y-%m-%d").strftime("%Y-%m-%d")

        date_from = datetime.strptime(str(data.get('start_date')), "%Y-%m-%d").strftime("%d-%m-%Y")
        date_to = datetime.strptime(str(data.get('end_date')), "%Y-%m-%d").strftime("%d-%m-%Y")
        company_id = self.env['res.company'].browse(data.get('company_id')[0])
        data = {
            'start_date': start_date,
            'date_from': date_from,
            'end_date': end_date,
            'date_to': date_to,
            'company_id': company_id,
            'remove_freebies': data.get('remove_freebies')
        }
        worksheet.merge_range(1, 0, 1, 21, TITLEHEDER, header_format)
        rowscol = 1
        worksheet.merge_range((rowscol + 1), 0, (rowscol + 1), 21, str(company_id.name), title_format)
        worksheet.merge_range((rowscol + 2), 0, (rowscol + 2), 21, str(date_from)+" - "+str(date_to), title_format)

        worksheet.write((rowscol + 4), 0, 'Warehouse', title_format)
        worksheet.write((rowscol + 4), 1, 'Invoice No', title_format)
        worksheet.write((rowscol + 4), 2, 'Invoice Date', title_format)
        worksheet.write((rowscol + 4), 3, 'Voucher Type', title_format)
        worksheet.write((rowscol + 4), 4, 'Party Name', title_format)
        worksheet.write((rowscol + 4), 5, 'Item Code', title_format)
        worksheet.write((rowscol + 4), 6, 'Item name', title_format)
        worksheet.write((rowscol + 4), 7, 'Attribute Value', title_format)
        worksheet.write((rowscol + 4), 8, 'Category', title_format)
        worksheet.write((rowscol + 4), 9, 'Label Category', title_format)
        worksheet.write((rowscol + 4), 10, 'Sale Order', title_format)
        worksheet.write((rowscol + 4), 11, 'Ordered QTY', title_format)
        worksheet.write((rowscol + 4), 12, 'Ordered Value', title_format)
        worksheet.write((rowscol + 4), 13, 'Billed Qty', title_format)
        worksheet.write((rowscol + 4), 14, 'Billed Value', title_format)
        worksheet.write((rowscol + 4), 15, 'Pending Qty', title_format)
        worksheet.write((rowscol + 4), 16, 'Pending Value', title_format)
        worksheet.write((rowscol + 4), 17, 'Discount Value', title_format)
        worksheet.write((rowscol + 4), 18, 'Area', title_format)
        worksheet.write((rowscol + 4), 19, 'Sales Person', title_format)
        worksheet.write((rowscol + 4), 20, 'Tag', title_format)
        worksheet.write((rowscol + 4), 21, 'ASM', title_format)
        rows = (rowscol + 5)
        for record in self.get_sale_details(data):
            worksheet.write(rows, 0, record.get('warehouse'), cell_wrap_format)
            worksheet.write(rows, 1, record.get('invoice_no'), cell_wrap_format)
            worksheet.write(rows, 2, record.get('invoice_date'), cell_wrap_format)
            worksheet.write(rows, 3, record.get('voucher_type'), cell_wrap_format)
            worksheet.write(rows, 4, record.get('party_name'), cell_wrap_format)
            worksheet.write(rows, 5, record.get('item_code'), cell_wrap_format)
            worksheet.write(rows, 6, record.get('item_name'), cell_wrap_format)
            worksheet.write(rows, 7, record.get('attribute_value'), cell_wrap_format)
            worksheet.write(rows, 8, record.get('category'), cell_wrap_format)
            worksheet.write(rows, 9, record.get('label_category'), cell_wrap_format)
            worksheet.write(rows, 10, record.get('sale_order_no'), cell_wrap_format)
            worksheet.write(rows, 11, record.get('ordered_qty'), cell_wrap_format_amount)
            worksheet.write(rows, 12, record.get('ordered_value'), cell_wrap_format_amount)
            worksheet.write(rows, 13, record.get('billed_qty'), cell_wrap_format_amount)
            worksheet.write(rows, 14, record.get('billed_value'), cell_wrap_format_amount)
            worksheet.write(rows, 15, record.get('pending_qty'), cell_wrap_format_amount)
            worksheet.write(rows, 16, record.get('pending_value'), cell_wrap_format_amount)
            worksheet.write(rows, 17, record.get('discount_value'), cell_wrap_format_amount)
            worksheet.write(rows, 18, record.get('area'), cell_wrap_format)
            worksheet.write(rows, 19, record.get('sales_person'), cell_wrap_format)
            worksheet.write(rows, 20, record.get('tag'), cell_wrap_format)
            worksheet.write(rows, 21, record.get('asm'), cell_wrap_format)
            rows = rows + 1

        workbook.close()
        buf = base64.b64encode(open('/tmp/' + file_path, 'rb+').read())
        self.document = buf
        self.file = 'Base Report' + '.xlsx'
        return {
            'res_id': self.id,
            'name': 'Files to Download',
            'view_type': 'form',
            "view_mode": 'form,tree',
            'res_model': 'sale.invoice.report.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
        }





