# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _default_partners_ids(self):
        domain = [('module', '=', 'dev_customer_credit_limit'), ('name',
                                                                 '=', 'credit_limit_config'), ('model', '=', 'res.groups')]
        imd = self.env['ir.model.data'].search(domain, limit=1)
        if imd:
            rg = self.env['res.groups'].browse(imd.res_id)
            return rg.users.partner_id
        else:
            return False

    patrners_ids = fields.Many2many('res.partner', 'order_partner_rel',
                                    'order_id', 'partner_id', 'Partners', default=_default_partners_ids)

    def compute_patrners_ids(self):
        partners = ''
        count = 0
        for partner in self.patrners_ids:
            count += 1
            if count == 1:
                partners += str(partner.id)
            else:
                partners += ', ' + str(partner.id)
        return partners
