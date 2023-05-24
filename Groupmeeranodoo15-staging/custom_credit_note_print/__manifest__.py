# -*- coding: utf-8 -*-
{
    'name': "custom_credit_note_print",

    'summary': """
        1.Hide Quantity in default credit note print""",

    'description': """
       
    """,
    'author': "Loyal IT Solutions PVT LTD",
    'website': "http://www.loyalitsolutions.com.com",
    'category': 'Sale',
    'version': '15.0.0.1',
    'depends': ['base','account','sale','l10n_in'],
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
