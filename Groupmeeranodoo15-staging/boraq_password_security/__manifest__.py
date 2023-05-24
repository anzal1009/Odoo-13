{

    'name': 'Password Security',
    "summary": "Allow admin to set password security requirements.",
    'version': '14.0.1.0.0',
    'author':
        "LasLabs, "
        "Kaushal Prajapati, "
        "Tecnativa, "
        "initOS GmbH, "
        "Boraq-Group, "
        "Odoo Community Association (OCA)",
    'category': 'Base',
    'depends': [
        'auth_signup',
        'auth_password_policy_signup',
    ],
    'external_dependencies': {
        'python': ['zxcvbn'],
    },
    "website": "https://github.com/OCA/server-auth",
    "license": "LGPL-3",
    "images": ['static/description/cover.png'],
    "data": [
        'views/password_security.xml',
        'views/res_company_view.xml',
        'views/res_config_settings_views.xml',
        'security/ir.model.access.csv',
        'security/res_users_pass_history.xml',
    ],
    'assets': {
        'web.assets_common': [
            'boraq_password_security/static/src/js/password_gauge.js',
            'boraq_password_security/static/lib/zxcvbn/zxcvbn.min.js'
        ],
    },
    "demo": [
        'demo/res_users.xml',
    ],
    'installable': True,
}
