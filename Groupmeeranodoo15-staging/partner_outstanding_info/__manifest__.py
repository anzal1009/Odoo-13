# -*- coding: utf-8 -*-
# Part of Odoo, Aktiv Software PVT. LTD.
# See LICENSE file for full copyright & licensing details.

# Author: Aktiv Software PVT. LTD.
# mail: odoo@aktivsoftware.com
# Copyright (C) 2015-Present Aktiv Software PVT. LTD.
# Contributions:
#   Aktiv Software:
#       - Aarti Sathvara
#       - Burhan Vakharia
#       - Tanvi Gajera
{
    "name": "Partner Outstanding Payment Information / Statement",
    "summary": """
        This module allows a user to get all the outstanding payment statements
        of partner in partner view.The data will be fetch at Runtime.
        Account,
        Payment,
        Statement,
        Information,
        Outstanding Payment,
        Partner Statement,
        Partner Statement Report,
        Outstanding Report,
        Customer Outstanding,
        Vendor Outstanding,
        Customer Overdue,
        Vendor Overdue,
        Partner Overdue,
        Overdue Report,
        Pending Invoices Report,
        Customer Pending Balance,
        Balance Information,
        Partner Balance,
        Supplier Outstanding,
        Supplier Overdue Report,
        Supplier Report,
        Supplier Statement,
        Supplier Pending Balance,
        OnScreen Statement Information,
        Generate Customer Statement,
        Generate Vendor Statement,
        Get partner pending invoices,
        Get supplier pending invoices,
        Get customer pending invoices,
     """,
    "description": """
        This module allows a user to get all the outstanding payement
        statements of partner in thier form view.Calculate the total
        outstanding amount and total balance of the partner.User can print
        the report of outstanding payment statement.
        Account,
        Payment,
        Statement,
        Information,
        Outstanding Payment,
        Partner Statement,
        Partner Statement Report,
        Outstanding Report,
        Customer Outstanding,
        Vendor Outstanding,
        Customer Overdue,
        Vendor Overdue,
        Partner Overdue,
        Overdue Report,
        Pending Invoices Report,
        Customer Pending Balance,
        Balance Information,
        Partner Balance,
        Supplier Outstanding,
        Supplier Overdue Report,
        Supplier Report,
        Supplier Statement,
        Supplier Pending Balance,
        OnScreen Statement Information,
        Generate Customer Statement,
        Generate Vendor Statement,
        Get partner pending invoices,
        Get supplier pending invoices,
        Get customer pending invoices,
    """,
    "author": "Aktiv Software",
    "website": "http://www.aktivsoftware.com",
    "category": "Account",
    "version": "15.0.1.0.0",
    "depends": ["account"],
    "license": "AGPL-3",
    "price": 15.00,
    "currency": "EUR",
    "data": [
        "views/res_partner_view.xml",
        "report/report.xml",
        "report/report_template.xml",
    ],
    "images": ["static/description/banner.jpg"],
}
