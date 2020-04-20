# -*- coding: utf-8 -*-
{
    'name': "notification budget suprapak",

    'summary': "",

    'description': "This is a module for Suprapak",

    'author': "Todoo",
    'website': "http://www.todoo.co",
    'contributors': "Livingston Arias la@todoo,co",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Purchase',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': ['purchase'],

    # always loaded
    'data': [
        # 'views/invoice_template.xml',
        'wizard/budget_wizard.xml',
         'views/budget_template.xml'
    ],
    # only loaded in demonstration mode
    'images': [],
    'application': True,
}