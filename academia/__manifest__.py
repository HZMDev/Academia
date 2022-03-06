# -*- coding: utf-8 -*-
{
    'name': "Academia",

    'summary': """
        Gestion de tu academia.""",

    'description': """
        Con este modulo se consigue gestionar una academia de forma eficiente y sencilla.
    """,

    'author': "Eduardo Delgado",
    'website': "http://www.github.com/HZMDev",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Administration',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/academia_security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        #'data/academia_data.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    
    'application': True,
}
