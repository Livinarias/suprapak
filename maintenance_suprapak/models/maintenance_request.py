# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TypeOfFailure(models.Model):
    _name = 'type.of.failure'
    _description = 'model for the types of failures'

    name = fields.Char("Name")
    maintenance_equipment_id = fields.Many2one('maintenance.equipment', string="Equipment")


class MaintenanceReques(models.Model):
    _inherit = 'maintenance.request'

    failure_id = fields.Many2one('type.of.failure',string="Type of failure")
