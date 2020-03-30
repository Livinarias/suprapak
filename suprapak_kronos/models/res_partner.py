# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResSector(models.Model):
    _name = 'res.sector'
    _description = 'Sector of Customer'

    name = fields.Char('Sector')
    code = fields.Char('code')


class ResPartner(models.Model):
    _inherit = 'res.partner'

    sector_id = fields.Many2one('res.sector')
    sectors_ids = fields.Many2many('res.sector','parner_sector_rel','res_sector_id','sector_id','Sectors')