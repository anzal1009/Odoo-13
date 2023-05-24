# -*- coding: utf-8 -*-
{
    'name': "Sales Return",

    'summary': """
        This module allows user to create sale return and can also return stock from same window after that user can 
        create credit note.""",

    'description': """
        This module allows user to create sale return and can also return stock from same window after that user can 
        create credit note.
    """,

    'author': "Loyal IT Solutions Pvt Ltd",
    'website': "http://www.loyalitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales/Return',
    'version': '15.0.1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'stock'],

    # always loaded
    'data': [
        'security/sales_return_security.xml',
        'security/ir.model.access.csv',
        # 'security/dismantle_process_security.xml',
        'data/sales_return_data.xml',
        'views/views.xml',
        'views/sale_return_reason_views.xml',
        # 'views/dismantle_views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
