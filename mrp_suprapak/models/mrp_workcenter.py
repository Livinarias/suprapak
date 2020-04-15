# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MrpWorkcenter(models.Model):
    _inherit = 'mrp.workcenter'

    costs_hour_mod = fields.Float('MOD per hour', help='Workforce cost', default=0.0)
    costs_hour_cif = fields.Float('CIF per hour', help='Indirect manufacturing costs', default=0.0)
    costs_hour_maq = fields.Float('Machine per hour', help='Machinery cost', default=0.0)
    mod_account_id = fields.Many2one('account.account', 'MOD account')
    cif_account_id = fields.Many2one('account.account', 'CIF account')
    maq_account_id = fields.Many2one('account.account', 'MAQ account')
    process_account_id = fields.Many2one('account.account', 'Process Product')
    
    @api.onchange('costs_hour_mod', 'costs_hour_cif', 'costs_hour_maq')
    def _onchange_costs(self):
        self.costs_hour = self.costs_hour_mod + self.costs_hour_cif + self.costs_hour_maq

    def _prepare_move_line(self):
        line_ids = []
        credit = 0.00
        partner_id = self.company_id.partner_id.id
        if self.costs_hour_mod and self.mod_account_id:
            line = {
                'name': 'Mano de obra',
                'partner_id': partner_id,
                'debit': self.costs_hour_mod,
                'credit': 0.00,
                'account_id': self.mod_account_id.id
            }
            line_ids.append((0,0,line))
            credit += self.costs_hour_mod
        if self.costs_hour_cif and self.cif_account_id:
            line = {
                'name': 'Costo indirecto de fabricacion',
                'partner_id': partner_id,
                'debit': self.costs_hour_cif,
                'credit': 0.00,
                'account_id': self.cif_account_id.id
            }
            line_ids.append((0,0,line))
            credit += self.costs_hour_cif
        if self.costs_hour_maq and self.maq_account_id:
            line = {
                'name': 'Maquinaria',
                'partner_id': partner_id,
                'debit': self.costs_hour_maq,
                'credit': 0.00,
                'account_id': self.maq_account_id.id
            }
            line_ids.append((0,0,line))
            credit += self.costs_hour_maq
        if credit > 0.00:
            line = {
                'name': 'Producto en proceso',
                'partner_id': partner_id,
                'debit': 0.00,
                'credit': credit,
                'account_id': self.process_account_id.id
            }
            line_ids.append((0,0,line))
        return line_ids
