# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = "res.company"

    msme_payment_term_id = fields.Many2one('account.payment.term', 'Payment Term for MSME Vendors',
                                                  domain="[('company_id', 'in', [id, False]), ('active', '=', True)]",
                                                  help='Default payment term for MSME vendors')


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    msme_payment_term_id = fields.Many2one('account.payment.term', 'Payment Term for MSME Vendors',
                                           domain="[('company_id', 'in', [id, False]), ('active', '=', True)]",
                                           help='Default payment term for MSME vendors', readonly=False,
                                           related="company_id.msme_payment_term_id")





