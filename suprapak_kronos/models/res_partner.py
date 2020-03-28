# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResSector(models.Model):
    _name = 'res.sector'
    _description = 'Sector of Customer'

    name = fields.Char('Sector')
    code = fields.Char('code')
