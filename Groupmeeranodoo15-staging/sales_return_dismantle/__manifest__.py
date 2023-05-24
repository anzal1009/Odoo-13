# -*- coding: utf-8 -*-
{
    'name': "Sales Return Quality Check",

    'summary': """
        Quality check of product after sales return""",

    'description': """
        Quality check of product after sales return
    """,

    'author': "Loyal It Solutions Pvt Ltd",
    'website': "http://www.loyalitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales/Return',
    'version': '15.0.1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'stock', 'mrp', 'sales_return'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/dismantle_process_security.xml',
        'data/dismantle_data.xml',
        'views/views.xml',
        'views/sales_return_view.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
