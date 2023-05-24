# -*- coding: utf-8 -*-
{
    'name': "Sequence based on Warehouse/ Location",

    'summary': """
        Sequence of invoice, credit note, debit note based on warehouse selected in moves and company address in invoice print as warehouse address.
        Sequence of internal transfer based on source location""",

    'description': """
        Sequence of invoice, credit note, debit note based on warehouse selected in moves and company address in invoice print as warehouse address.
        Sequence of internal transfer based on source location
    """,

    'author': "Loyal IT Solutions Pvt Ltd",
    'website': "http://www.loyalitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '15.0.1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'stock', 'default_invoice_print', 'web', 'sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
