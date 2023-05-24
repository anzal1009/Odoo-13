# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict
from odoo import fields, models,_,api
from odoo.exceptions import UserError
from datetime import date




class BarcodeProductLabelLayout(models.TransientModel):
    _name = 'product.labels'


    print_format = fields.Selection([
        ('label1', 'Sunidra Print'),
        ('label2', 'Small Print'),
        ('label3', 'DTC'),
        ('label4', 'Ruby'),
        ], string="Format", default='label1', required=True)
    custom_quantity = fields.Integer('Quantity', default=1, required=True)
    product_id = fields.Many2one('product.product',required=True)
    product_tmpl_id = fields.Many2one('product.template')
    extra_html = fields.Html('Extra Content', default='')
    rows = fields.Integer(compute='_compute_dimensions')
    columns = fields.Integer(compute='_compute_dimensions')

    # product_template_attribute_value_ids = fields.Many2many('product.template.attribute.value',related='product_id.product_template_attribute_value_ids',string="Attribute Values",)
    product_template_attribute_value_ids = fields.Many2one('product.template.attribute.value',string="Attribute Values",)
    # product_template_attribute_value_ids = fields.Many2one(related='product_id.product_template_attribute_value_ids.id', string="Attribute Values",)
    price_list_item = fields.Many2one('product.pricelist.item', string="Pricelist",)

    @api.onchange('product_id')
    def domain_pricelist_product_id(self):
        if self.product_id:

            product_attribute_ids = self.env['product.template.attribute.value'].search(
                [('attribute_id.label_print', '=', True), ('product_tmpl_id', 'in',self.product_id.product_tmpl_id.ids)])

            return {'domain': {'product_template_attribute_value_ids': [('id', 'in', product_attribute_ids.ids)]}}

    # @api.onchange('product_id')
    # def domain_pricelist_product_id(self):
    #     if self.product_id:
    #         product_template_ids = self.env['product.template'].search(
    #             [('pricelist_id', '=', self.product_id.pricelist_id.id)])
    #         product_template_ids = self.env['product.product'].search(
    #             [('pricelist_id', '=', self.product_id.pricelist_id.id)])
    #         # .filtered(
    #         # # lambda   product_template_ids = self.env['product.template'].search([]).filtered(
    #         # lambda x: self.product_id.pricelist_id.id in x.item_ids.mapped('pricelist_id').ids)
    #         product_ids = self.env['product.pricelist.item'].search(
    #             [('product_id', 'in', self.product_id.ids)])
    #         return {'domain': {'price_list_item': [('id', 'in', product_ids.ids)]}}

    # domain = "[('id', 'in', product_id.product_template_attribute_value_ids)]",
    categ_id = fields.Many2one('product.category', 'Product Category')
    sub_categ_id = fields.Many2one('product.category', 'Sub Product Category')
    dimensions = fields.Char(string='Dimensions')
    content = fields.Char(string='Content')
    date = fields.Date(string='Date', default=date.today())

    label1_state = fields.Selection([
        ('KL', 'Kerala'),
        # ('TM', 'Tamil Nadu,Karnataka & Pondicherry'),
        ('KA', 'Karnataka'),
        ('TM', 'Tamil Nadu'),
        ('AN', 'Andhrapradesh & Telagana'),
        ('AP', 'Rest of India'),
        # ('MH', 'Maharashtra,Chattisgarh,Madhya Pradesh & GOA'),
        # ('GJ', 'Gujarat'),
        # ('RJ', 'Rajasthan'),
        # ('UP', 'Uttar Pradesh'),
        # ('PB', 'Punjab'),
        # ('DL', 'Delhi,Haryana,Jammu and Kashmir,Himachal Pradesh,Chandigarh and Uttaranchal'),
        # ('WB', 'Orissa,Bihar,Jharkhand and West Bengal'),
        # ('AR', 'Nagaland,Assam,Meghalaya,Arunachal Pradesh,Manipur,Mizoram,Sikkim And Tripura'),
    ], string="State", default='KL')
    label2_state = fields.Selection([
        ('KL', 'Kerala'),
        ('TM', 'Tamil Nadu & Pondicherry'),
        ('AN', 'Andhrapradesh & Telagana'),
        ('KA', 'Karnataka'),
        ('GO', 'GOA'),
        ('MH', 'Maharashtra'),
    ], string="State", default='KL')

    manual_print = fields.Selection([
        ('labels', 'Label Print'),
        ('manual', 'Manual Print'),
    ], string="Manual Print",default='labels')

    serial_no = fields.Char(string='Serial Number')
    company_id = fields.Many2one('res.company', string='Company',default=lambda self: self.env.company)

    product_mrp = fields.Float(string="MRP",)
    label_category = fields.Many2one('label.category', string='Label Category')

    @api.onchange('manual_print')
    def _onchange_manual_print(self):
        for i in self:
            i.custom_quantity = 1

    @api.onchange('product_id')
    def _onchange_product(self):
        for i in self:
            if i.product_id:
                i.dimensions=i.product_id.dimensions
                i.content = i.product_id.content
                i.categ_id =i.product_id.categ_id
                i.product_mrp =i.product_id.product_mrp
                i.label_category =i.product_id.label_category.id


    @api.depends('print_format')
    def _compute_dimensions(self):
        for wizard in self:
            if 'x' in wizard.print_format:
                columns, rows = wizard.print_format.split('x')[:2]
                wizard.columns = int(columns)
                wizard.rows = int(rows)
            else:
                wizard.columns, wizard.rows = 1, 1



    def _prepare_report_data(self):
        if self.custom_quantity <= 0:
            raise UserError(_('You need to set a positive quantity.'))

        # Get layout grid
        if self.print_format == 'label1':
            xml_id = 'barcode_label_print.report_product_label1'
        elif self.print_format =='label2':
            xml_id = 'barcode_label_print.report_product_label2'
        elif self.print_format =='label3':
            xml_id = 'barcode_label_print.report_product_label3'
        elif self.print_format == 'label4':
            xml_id = 'barcode_label_print.report_product_label4'
        else:
            xml_id = ''

        active_model = ''
        products = self.ids
        active_model = 'product.labels'

        # Build data to pass to the report
        data = {
            'active_model': active_model,
            'quantity_by_product': {p: self.custom_quantity for p in products},
            'layout_wizard': self.id,
            'price_included': 'xprice' in self.print_format,
            'print_format':self.print_format
        }
        return xml_id, data

    # if self.picking_quantity == 'picking' and self.move_line_ids:
    #     qties = defaultdict(int)
    #     custom_barcodes = defaultdict(list)
    #     uom_unit = self.env.ref('uom.product_uom_categ_unit', raise_if_not_found=False)
    #     for line in self.move_line_ids:
    #         if line.product_uom_id.category_id == uom_unit:
    #             if (line.lot_id or line.lot_name) and int(line.qty_done):
    #                 custom_barcodes[line.product_id.id].append((line.lot_id.name or line.lot_name, int(line.qty_done)))
    #                 continue
    #             qties[line.product_id.id] += line.qty_done
    #     # Pass only products with some quantity done to the report
    #     data['quantity_by_product'] = {p: int(q) for p, q in qties.items() if q}
    #     data['custom_barcodes'] = custom_barcodes



    def serial_updation(self,serials):
        for i in self:
            i.product_id.serial_no = serials


    def process(self):
        self.ensure_one()
        xml_id, data = self._prepare_report_data()
        if not xml_id:
            raise UserError(_('Unable to find report template for %s format', self.print_format))
        return self.env.ref(xml_id).report_action(None, data=data)
    # def company_url(self,barcode_sl):
    # def company_url(self,barcode_sl):
    def company_url(self,suffix,serial_no):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        # base_url = self.env['ir.config_parameter'].sudo().get_param('report.url') or self.env['ir.config_parameter'].sudo().get_param('web.base.url')

        # url = base_url+'/warranty_registration/'+barcode_sl
        # url = base_url + '/warranty_registration/' + suffix + str(serial_no)

        for i in self:
            if i.manual_print=='manual':
                url = base_url + '/wr/' + suffix + '/' + str(serial_no).replace(suffix,'')
            else:
                url = base_url+'/wr/'+suffix+'/'+str(serial_no)
        return url

