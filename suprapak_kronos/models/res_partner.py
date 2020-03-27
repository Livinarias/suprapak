# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Sector(models.Model):
    _name = 'sector'
    _description = 'Sector of Customer'

    name = fields.Char('Sector')
    code = fields.Char('code')
