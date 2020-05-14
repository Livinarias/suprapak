# -*- coding: utf-8 -*-
from odoo import fields, models, http, _, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def write(self, vals):
        res = super(SaleOrder, self).write(vals)
        for record in self:
            result = self.env['account.tax'].browse()
            tax_count_out = 0
            for line in record.order_line:
                taxes = line.product_id.taxes_id.filtered(
                    lambda r: not record.company_id or r.company_id == record.company_id)
                fpos = record.partner_id.property_account_position_id
                for tax in taxes:
                    tax_count = 0
                    for t in fpos.tax_ids:
                        if t.tax_src_id == tax:
                            if t.condition_type and t.amount > 0:
                                if t.condition_type == '<':
                                    if record.amount_untaxed < t.amount:
                                        tax_count += 1
                                        tax_count_out += 1
                                        result |= t.tax_dest_id
                                elif t.condition_type == '<=':
                                    if record.amount_untaxed <= t.amount:
                                        tax_count += 1
                                        tax_count_out += 1
                                        result |= t.tax_dest_id
                                elif t.condition_type == '>':
                                    if record.amount_untaxed > t.amount:
                                        tax_count += 1
                                        tax_count_out += 1
                                        result |= t.tax_dest_id
                                elif t.condition_type == '>=':
                                    if record.amount_untaxed >= t.amount:
                                        tax_count += 1
                                        tax_count_out += 1
                                        result |= t.tax_dest_id
                if not tax_count:
                    line.tax_id = tax
            if tax_count_out:
                record.order_line.write({'tax_id':result})
        return res

    @api.model
    def create(self, vals):
        res = super(SaleOrder, self).create(vals)
        for record in res:
            result = self.env['account.tax'].browse()
            tax_count_out = 0
            for line in record.order_line:
                taxes = line.product_id.taxes_id.filtered(
                    lambda r: not record.company_id or r.company_id == record.company_id)
                fpos = record.partner_id.property_account_position_id
                for tax in taxes:
                    tax_count = 0
                    for t in fpos.tax_ids:
                        if t.tax_src_id == tax:
                            if t.condition_type and t.amount > 0:
                                if t.condition_type == '<':
                                    if record.amount_untaxed < t.amount:
                                        tax_count += 1
                                        tax_count_out += 1
                                        result |= t.tax_dest_id
                                elif t.condition_type == '<=':
                                    if record.amount_untaxed <= t.amount:
                                        tax_count += 1
                                        tax_count_out += 1
                                        result |= t.tax_dest_id
                                elif t.condition_type == '>':
                                    if record.amount_untaxed > t.amount:
                                        tax_count += 1
                                        tax_count_out += 1
                                        result |= t.tax_dest_id
                                elif t.condition_type == '>=':
                                    if record.amount_untaxed >= t.amount:
                                        tax_count += 1
                                        tax_count_out += 1
                                        result |= t.tax_dest_id
                if not tax_count:
                    line.tax_id = tax
            if tax_count_out:
                record.order_line.write({'tax_id': result})
        return res


# class SaleOrderLine(models.Model):
#     _inherit = 'sale.order.line'
#
#     @api.onchange('product_uom_qty', 'price_unit')
#     def onchange_price_qty(self):
#         if self.product_uom_qty and self.product_id and self.price_unit:
#             result = self.env['account.tax'].browse()
#             total_amount = self.price_unit * self.product_uom_qty
#             taxes = self.product_id.taxes_id.filtered(lambda r: not self.company_id or r.company_id == self.company_id)
#             fpos = self.order_id.partner_id.property_account_position_id
#             for tax in taxes:
#                 tax_count = 0
#                 for t in fpos.tax_ids:
#                     if t.tax_src_id == tax:
#                         if t.condition_type and t.amount > 0:
#                             if t.condition_type == '<':
#                                 if total_amount < t.amount:
#                                     tax_count += 1
#                                     # if t.tax_dest_id:
#                                     result |= t.tax_dest_id
#                             elif t.condition_type == '<=':
#                                 if total_amount <= t.amount:
#                                     # if t.tax_dest_id:
#                                     tax_count += 1
#                                     result |= t.tax_dest_id
#                             elif t.condition_type == '>':
#                                 if total_amount > t.amount:
#                                     # if t.tax_dest_id:
#                                     tax_count += 1
#                                     result |= t.tax_dest_id
#                             elif t.condition_type == '>=':
#                                 if total_amount >= t.amount:
#                                     # if t.tax_dest_id:
#                                     tax_count += 1
#                                     result |= t.tax_dest_id
#                 # if not tax_count:
#                 #     result |= tax
#             self.tax_id = result if fpos else taxes
