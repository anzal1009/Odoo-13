# -*- coding: utf-8 -*-
{
    'name': "Warranty Registration Portal",

    'summary': """
        Warranty Registration""",

    'description': """
        Warranty Registration
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
    'depends': ['base', 'portal', 'barcode_label_print', 'sale', 'product_warranty_axis'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/config.xml',
        'views/views.xml',
        'views/templates.xml',

    ],
    # 'assets': {
    #     'web.assets_frontend': [
    #         'warranty_registration_portal/static/src/js/portal.js',
    #     ],
    #
    # },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
