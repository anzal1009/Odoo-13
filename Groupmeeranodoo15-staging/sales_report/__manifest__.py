# -*- coding: utf-8 -*-
{
    'name': "DSR Report",

    'summary': """
        DSR Report""",

    'description': """
        DSR Report
    """,

    'author': "Loyal It solutions PVT Ltd",
    'website': "http://www.loyalitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    'license':'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','account','eastern_freebies'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/users.xml',
        'wizard/sale_report_wizard.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
