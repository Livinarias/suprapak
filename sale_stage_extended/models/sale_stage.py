# -*- coding: utf-8 -*-
from odoo import fields, models,http,_

class sale_quatation(models.Model):
    _inherit = "sale.order"

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('pre-conform', 'Pre-Conform'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')

    def action_confirm(self):
        if self.env.context.get('is_confrim', False):
            return super(sale_quatation, self).action_confirm()


