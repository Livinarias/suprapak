# -*- coding: utf-8 -*-
from odoo import fields, models, http, _


class StockMove(models.Model):
    _inherit = "stock.move"

    #price_unit = fields.Float(related='sale_line_id.price_unit', string='Price')
    price_unit = fields.Float(related='sale_line_id.price_unit', string='Total')


class StockPicking(models.Model):
    _inherit = "stock.picking"

    amount_untaxed = fields.Monetary(related='sale_id.amount_untaxed', string='Untaxed Amount', readonly=True)
    amount_tax = fields.Monetary(related='sale_id.amount_tax', string='Taxes', readonly=True)
    amount_total = fields.Monetary(related='sale_id.amount_total', string='Total', readonly=True)
    currency_id = fields.Many2one(related='sale_id.currency_id', string='Currency',
                                  readonly=True)
