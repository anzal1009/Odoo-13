# -*- coding: utf-8 -*-
# from odoo import http


# class AccountReportsIntervalPeriod(http.Controller):
#     @http.route('/account_reports_interval_period/account_reports_interval_period', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_reports_interval_period/account_reports_interval_period/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_reports_interval_period.listing', {
#             'root': '/account_reports_interval_period/account_reports_interval_period',
#             'objects': http.request.env['account_reports_interval_period.account_reports_interval_period'].search([]),
#         })

#     @http.route('/account_reports_interval_period/account_reports_interval_period/objects/<model("account_reports_interval_period.account_reports_interval_period"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_reports_interval_period.object', {
#             'object': obj
#         })
