# -*- coding: utf-8 -*-
{
    'name': "Payment Signature",
    'summary': """
        Payment Signature""",
    'description': """
        Payment Signature
    """,
    'author': 'MPTechnolabs',
    'website': 'http://www.mptechnolabs.com',
    'category': 'Employee',
    'version': '0.1',
    'depends': ['sale_stock', 'sign'],
    'data': [
        'data/email_template.xml',
        'views/account_payment_view.xml',
        'views/res_partner_view.xml',
    ],
}