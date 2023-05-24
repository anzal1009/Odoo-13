# -*- coding: utf-8 -*-
{
    'name': "Manufacturing Indent",

    'summary': """
        Create MRP Indents To Store Team.""",

    'description': """
        When we create a MRP Order, MRP team need raw material and if we confirm MO,
        an indent is created automatically and only indent approver can approve the indent and issue the stock.
    """,

    'author': "Loyal IT Solutions Pvt Ltd",
    'website': "http://www.loyalitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Manufacturing/Manufacturing',
    'version': '15.0.1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mrp', 'stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
        'security/indent_security.xml',
        'data/mrp_indent_data.xml',
        'views/views.xml',
        'views/mrp_production_views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
