# -*- coding: utf-8 -*-
{
    'name': "Invoice LYS",

    'summary': "",

    'description': "This is a module for Suprapak",

    'author': "Todoo",
    'website': "http://www.todoo.co",
    'contributors': "Livingston Arias la@todoo,co",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Account',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': ['account_accountant','contacts'],

    # always loaded
    'data': [
        # 'views/invoice_template.xml',
        # 'views/report_invoice_document_supra.xml',
         'views/res_partner.xml'
    ],
    # only loaded in demonstration mode
    'images': [],
    'application': True,
}