# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    lst_price_tyc = fields.Float('Public price Kanban', digits='Product Price')


class ProductProduct(models.Model):
    _inherit = 'product.product'

    lst_price_tyc = fields.Float('Public price Kanban', digits='Product Price')
