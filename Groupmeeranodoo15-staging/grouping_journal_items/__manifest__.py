# -*- coding: utf-8 -*-
{
    'name': "Grouping journal items",

    'summary': """
        Display and Print Journal Items Grouped by account in journal Entry form""",

    'description': """
        Display Journal Items Grouped by account inside journal Entry,
        Print Journal Items and Grouped by account journal entry
    """,

    'author': "Loyal IT Solutions Pvt Ltd",
    'website': "http://www.loyalitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting/Accounting',
    'version': '15.0.1',
    "license": "LGPL-3",

    # any module necessary for this one to work correctly
    'depends': ['base', 'web', 'account'],
    'external_dependencies': {
        'python': ['pandas'],
    },

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
