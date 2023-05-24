# -*- coding: utf-8 -*-

from odoo import models, fields, api


class WarrantyRegistration(models.Model):
    _name = "warranty.registration"
    _description = 'Warranty Registration'

    product_id = fields.Many2one('product.product', string="Product", required=True)
    customer_name = fields.Char(string="Name", required=True)
    phone = fields.Char(string="Phone No.", required=True)
    email = fields.Char(string="Email", required=True)
    state_id = fields.Many2one('res.country.state', string='State', required=True)
    city = fields.Char("City", required=True)
    pincode = fields.Char("Pincode", required=True)
    purchase_date = fields.Date("Purchase Date", required=True)
    contact_me = fields.Boolean("Contact Consent", required=True, default=True)
    attachment_ids = fields.Many2many('ir.attachment', 'res_id', string="Attachments")


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    attachment_ids = fields.Many2many('ir.attachment', relation='helpdesk_ticket_ir_attachments_rel', string="Attachments")




