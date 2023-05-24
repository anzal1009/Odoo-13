# -*- coding: utf-8 -*-
{
    'name': "barcode_label_print",

    'summary': """
        Barcode Label Print""",

    'description': """
        Barcode Label Print
    """,

    'author': "Loyal It Solutions Pvt Ltd",
    'website': "http://www.loyalitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base','product','sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/label_category.xml',
        'views/product.xml',
        'views/views.xml',
        'views/label_print.xml',
        'views/templates.xml',
        'views/label1.xml',
        'views/label2.xml',
        'views/label3.xml',
        'views/ruby.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
