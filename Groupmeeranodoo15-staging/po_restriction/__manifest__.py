# -*- coding: utf-8 -*-
{
    'name': "po_restriction",

    'summary': """
        restriction""",

    'description': """
       1.PO restiction for zero quandity and zero price in line 
       2.Restrict edit option of purchase line after confirm the PO
    """,

    'author': "Loyal it solutions pvt ltd",
    'website': "http://www.loyalitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','purchase'],

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
