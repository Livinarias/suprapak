# -*- coding: utf-8 -*-

{
    "name": "Odoo Background View",
    'version': '13.0.0.1.2',
    "category": "Theme/Backend",
    'author': 'Todoo SAS',
    'company': 'Todoo SAS',
    'maintainer': 'Todoo SAS',
    'website': 'https://www.todoo.co',
    "description": """Backend theme for Odoo 13.0 """,
    "summary": "Changing the background color",
#    'images': ['static/description/icon.png'],
    "installable": True,
    "depends": ['base'],
    "data": [
        'views/background_view.xml',
    ],
    'qweb': ['static/src/xml/*.xml'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
