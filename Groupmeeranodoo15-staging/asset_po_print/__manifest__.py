# -*- coding: utf-8 -*-
{
    'name': "asset_po_print",

    'summary': """
        Asset PO Print""",

    'description': """
        Asset PO Print
    """,

    'author': "Loyal It Solutions PVT Ltd",
    'website': "http://www.loyalitsolutions.com",


    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'eastern_po_print'],
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/product_seq.xml',
        'views/product_views.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
