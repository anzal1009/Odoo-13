# -*- coding: utf-8 -*-
from odoo import http, _, tools
from odoo.http import request
import base64
import datetime


class WarrantyRegistrationPortal(http.Controller):
    MANDATORY_BILLING_FIELDS = ["customer_name", "phone", "email", "state_id", "city", "pincode", "purchase_date", "product_id", "invoice_mrp_file", "contact_me"]



    @http.route('/wr/<string:suffix>/<string:hashed_serial>', type='http', auth='public', website=True)
    def warranty_registration(self, suffix, hashed_serial, **post):
        product_details = request.env['product.product'].sudo().search([('suffix', '=', suffix), ('serial_no', '=', int(hashed_serial))])
        if not product_details:
            product_details = request.env['stock.production.lot'].sudo().search([('name', '=', suffix+hashed_serial)],
                                                                                limit=1).product_id
        states = request.env['res.country.state'].sudo().search([])

        terms_and_conditions  = request.env["ir.config_parameter"].sudo().get_param(
            "warranty_registration_portal.terms_and_conditions")
        if terms_and_conditions:
            conditions= terms_and_conditions
        else:
            conditions =" "

        values = {
            'serial_number': suffix+hashed_serial,
            'product_details': product_details,
            'states': states,
            'lot_no': suffix+hashed_serial,
            'terms_and_conditions':conditions
        }
        # if post and request.httprequest.method == 'POST':
        #     error, error_message = self.details_form_validate(post)
        #     values.update({'error': error, 'error_message': error_message})
        return request.render('warranty_registration_portal.warranty_registration_portal_page', values)

    def details_form_validate(self, data):
        error = dict()
        error_message = []

        # Validation
        for field_name in self.MANDATORY_BILLING_FIELDS:
            if not data.get(field_name):
                error[field_name] = 'missing'

        # email validation
        if data.get('email') and not tools.single_email_re.match(data.get('email')):
            error["email"] = 'error'
            error_message.append(_('Invalid Email! Please enter a valid email address.'))

        # error message for empty required fields
        if [err for err in error.values() if err == 'missing']:
            error_message.append(_('Some required fields are empty.'))
        return error, error_message

    @http.route('/wr_form/submit', type='http', auth="public", methods=['POST'], website=True, csrf=False)
    def warranty_registration_submit_form(self, **post):

        # Attachments = request.env['ir.attachment']
        # name = post.get('invoice_mrp_file').filename
        # file = post.get('invoice_mrp_file')
        lot_id = request.env['stock.production.lot'].sudo().search(
            [('product_id.id', '=', int(post.get('product_id'))), ('name', '=', post.get('lot_no'))])
        existing_ticket = request.env['helpdesk.ticket'].sudo().search(
            [('product.id', '=', int(post.get('product_id'))), ('serial_number.id', '=', lot_id.id)])
        if not existing_ticket and lot_id:
            partner_id = request.env['res.partner'].sudo().search([('email', '=', post.get('email'))])
            if not partner_id:
                partner_id = request.env['res.partner'].sudo().create({
                    'name': post.get('customer_name'),
                    'email': post.get('email'),
                    'phone': post.get('phone'),
                    'state_id': int(post.get('state_id')),
                    'city': post.get('city'),
                    'zip': post.get('pincode')
                })
            if lot_id.warranty_year:
                format_str = '%Y%m%d'
                warranty_year = int(lot_id.warranty_year) * 365
                a = post.get('purchase_date')
                date_str = str(a).replace('-', '')
                start_date_info = datetime.datetime.strptime(date_str, format_str)
                end_date = start_date_info + datetime.timedelta(days=warranty_year)
            else:
                end_date = post.get('purchase_date')
            lot_id.write({
                'partner_id': partner_id.id,
                'partner_email': post.get('email'),
                'partner_phone': post.get('phone'),
                'start_date': post.get('purchase_date'),
                'end_date': end_date
            })

            ticket = request.env['helpdesk.ticket'].sudo().create({
                'name': lot_id.name,
                'partner_id': partner_id.id,
                'partner_name': post.get('customer_name'),
                'partner_email': post.get('email'),
                'partner_phone': post.get('phone'),
                'product': int(post.get('product_id')),
                'serial_number': lot_id.id,
                'warranty_year': lot_id.warranty_year,
                'start_date': post.get('purchase_date'),
                'end_date': end_date
            })

            warranty_registration = request.env['warranty.registration'].sudo().create({
                'customer_name': request.params.get('customer_name'),
                'phone': request.params.get('phone'),
                'email': request.params.get('email'),
                'state_id': int(request.params.get('state_id')),
                'city': request.params.get('city'),
                'pincode': request.params.get('pincode'),
                'purchase_date': request.params.get('purchase_date'),
                'product_id': int(request.params.get('product_id')),
                'contact_me': True
            })

            attached_files = request.httprequest.files.getlist('invoice_mrp_file')
            for attachment in attached_files:
                attached_file = attachment.read()
                file = request.env['ir.attachment'].sudo().create({
                    'name': attachment.filename,
                    'type': 'binary',
                    'datas': base64.b64encode(attached_file),
                    'res_model': 'warranty.registration',
                    'res_id': warranty_registration.id,
                })
                warranty_registration.write({'attachment_ids': [(4, file.id)]})
                file_ticket = request.env['ir.attachment'].sudo().create({
                    'name': attachment.filename,
                    'res_model': 'helpdesk.ticket',
                    'res_id': ticket.id,
                    'type': 'binary',
                    'datas': base64.b64encode(attached_file),
                })
                ticket.write({'attachment_ids': [(4, file_ticket.id)]})
            return request.render('warranty_registration_portal.warranty_registration_submitted')
        else:
            return request.render("product_warranty_axis.error_message_serial")




