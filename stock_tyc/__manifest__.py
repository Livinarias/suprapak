# -*- coding: utf-8 -*-
{
    'name': "Stock tyc",

    'summary': "Stock tyc",

    'description': "Stock tyc",

    'author': "Todoo SAS",
    'contributors': "Pablo Arcos pa@todoo,co",
    'website': "http://www.todoo.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Operations',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': ['stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/product_product_view.xml',
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
