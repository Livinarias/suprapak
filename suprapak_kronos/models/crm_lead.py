# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    sheet_count = fields.Integer('Number of sheets', compute='_compute_sheet_data')
    sheet_ids = fields.One2many('data.sheet', 'opportunity_id', 'Sheets')
    currency_id = fields.Many2one('res.currency', 'Currency', required=True)
    product_code = fields.Char('Product code', help='Customer product code', required=True)
    sector_id = fields.Many2one('res.sector', 'Sector', required=True)
    sector_code = fields.Char('Sector code')
    customer_zip = fields.Char('zip')

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            self.customer_zip = self.partner_id.zip

    @api.onchange('sector_id')
    def _onchange_sector_id(self):
        if self.sector_id:
            self.sector_code = self.sector_id.code

    def _compute_sheet_data(self):
        for lead in self:
            count = len(lead.sheet_ids)
            lead.sheet_count = count

    def action_new_data_sheet(self):
        name = ''
        """if self.type_sheet == 'quotation':
            name += 'C'
        if self.type_sheet == 'show':
            name += 'M'
        if self.type_sheet == 'sale':
            name += 'P'"""
        if self.sector_id:
            name += self.sector_id.code
        name += ' - ' + self.product_code
        action = self.env.ref("suprapak_kronos.action_new_data_sheet_new").read()[0]
        action['context'] = {
            'search_default_opportunity_id': self.id,
            'default_opportunity_id': self.id,
            'search_default_partner_id': self.partner_id.id,
            'default_partner_id': self.partner_id.id,
            'default_team_id': self.team_id.id,
            'default_company_id': self.company_id.id or self.env.company.id,
            'default_currency_id': self.currency_id.id,
            'default_product_code': self.product_code,
            'default_name': name,
            'default_sector_id': self.sector_id,
        }
        return action

    def action_view_data_sheet(self):
        action = self.env.ref('suprapak_kronos.action_data_sheet').read()[0]
        action['context'] = {
            'default_partner_id': self.partner_id.id,
            'default_opportunity_id': self.id
        }
        action['domain'] = [('opportunity_id', '=', self.id)]
        return action


class DataSectorType(models.Model):
    _name = 'data.sector.type'
    _description = 'Sector Type'

    name = fields.Char('Sector')
