# -*- coding: utf-8 -*-
from odoo import fields, models, http, _, api


class AccountFiscalPositionTax(models.Model):
    _inherit = 'account.fiscal.position.tax'

    condition_type = fields.Selection([
        ('>', '>'),
        ('<', '<'),
        ('>=', '>='), ('<=', '<=')], default='>')
    amount = fields.Float('Total Amount')


class AccountMove(models.Model):
    _inherit = "account.move"

    # def write(self, vals):
    #     res = super(AccountMove, self).write(vals)
    #     for record in self:
    #         result = self.env['account.tax'].browse()
    #         tax_count_out = 0
    #         for line in record.invoice_line_ids:
    #             taxes = line.tax_ids.filtered(
    #                 lambda r: not record.company_id or r.company_id == record.company_id)
    #             fpos = record.partner_id.property_account_position_id
    #             for tax in taxes:
    #                 tax_count = 0
    #                 for t in fpos.tax_ids:
    #                     if t.tax_src_id == tax:
    #                         if t.condition_type and t.amount > 0:
    #                             if t.condition_type == '<':
    #                                 if record.amount_untaxed < t.amount:
    #                                     tax_count += 1
    #                                     tax_count_out += 1
    #                                     result |= t.tax_dest_id
    #                             elif t.condition_type == '<=':
    #                                 if record.amount_untaxed <= t.amount:
    #                                     tax_count += 1
    #                                     tax_count_out += 1
    #                                     result |= t.tax_dest_id
    #                             elif t.condition_type == '>':
    #                                 if record.amount_untaxed > t.amount:
    #                                     tax_count += 1
    #                                     tax_count_out += 1
    #                                     result |= t.tax_dest_id
    #                             elif t.condition_type == '>=':
    #                                 if record.amount_untaxed >= t.amount:
    #                                     tax_count += 1
    #                                     tax_count_out += 1
    #                                     result |= t.tax_dest_id
    #                 if not tax_count:
    #                     print ('--------call-------call----------')
    #                     line.tax_ids = tax
    #         if tax_count_out:
    #             print ("result ______________",result)
    #             record.invoice_line_ids.write({'tax_ids': [(6,0, result.ids or [])]})
    #             record._compute_invoice_taxes_by_group()
    #     return res

    # @api.model
    # def create(self, vals):
    #     res = super(SaleOrder, self).create(vals)
    #     for record in res:
    #         result = self.env['account.tax'].browse()
    #         tax_count_out = 0
    #         for line in record.order_line:
    #             taxes = line.product_id.taxes_id.filtered(
    #                 lambda r: not record.company_id or r.company_id == record.company_id)
    #             fpos = record.partner_id.property_account_position_id
    #             for tax in taxes:
    #                 tax_count = 0
    #                 for t in fpos.tax_ids:
    #                     if t.tax_src_id == tax:
    #                         if t.condition_type and t.amount > 0:
    #                             if t.condition_type == '<':
    #                                 if record.amount_untaxed < t.amount:
    #                                     tax_count += 1
    #                                     tax_count_out += 1
    #                                     result |= t.tax_dest_id
    #                             elif t.condition_type == '<=':
    #                                 if record.amount_untaxed <= t.amount:
    #                                     tax_count += 1
    #                                     tax_count_out += 1
    #                                     result |= t.tax_dest_id
    #                             elif t.condition_type == '>':
    #                                 if record.amount_untaxed > t.amount:
    #                                     tax_count += 1
    #                                     tax_count_out += 1
    #                                     result |= t.tax_dest_id
    #                             elif t.condition_type == '>=':
    #                                 if record.amount_untaxed >= t.amount:
    #                                     tax_count += 1
    #                                     tax_count_out += 1
    #                                     result |= t.tax_dest_id
    #             if not tax_count:
    #                 line.tax_id = tax
    #         if tax_count_out:
    #             record.order_line.write({'tax_id': result})
    #     return res

# class AccountFiscalPosition(models.Model):
#     _inherit = 'account.fiscal.position'

# @api.model  # noqa
# def map_tax(self, taxes, product=None, partner=None):
#     result = self.env['account.tax'].browse()
#     total_amount = product.lst_price * 1
#     for tax in taxes:
#         tax_count = 0
#         for t in self.tax_ids:
#             if t.tax_src_id == tax:
#                 if t.condition_type and t.amount > 0:
#                     if t.condition_type == '<':
#                         if total_amount < t.amount:
#                             tax_count += 1
#                             if t.tax_dest_id:
#                                 result |= t.tax_dest_id
#                     elif t.condition_type == '<=':
#                         if total_amount <= t.amount:
#                             if t.tax_dest_id:
#                                 tax_count += 1
#                                 result |= t.tax_dest_id
#                     elif t.condition_type == '>':
#                         if total_amount > t.amount:
#                             if t.tax_dest_id:
#                                 tax_count += 1
#                                 result |= t.tax_dest_id
#                     elif t.condition_type == '>=':
#                         if total_amount >= t.amount:
#                             if t.tax_dest_id:
#                                 tax_count += 1
#                                 result |= t.tax_dest_id
#         if not tax_count:
#             result |= tax
#     return result
