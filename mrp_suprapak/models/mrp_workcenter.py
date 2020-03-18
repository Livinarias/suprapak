# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MrpWorkcenter(models.Model):
    _inherit = 'mrp.workcenter'

    costs_hour_mod = fields.Float('MOD per hour', help='Workforce cost', default=0.0)
    costs_hour_cif = fields.Float('CIF per hour', help='Indirect manufacturing costs', default=0.0)
    costs_hour_maq = fields.Float('Machine per hour', help='Machinery cost', default=0.0)
    
    @api.onchange('costs_hour_mod', 'costs_hour_cif', 'costs_hour_maq')
    def _onchange_costs(self):
        self.costs_hour = self.costs_hour_mod + self.costs_hour_cif + self.costs_hour_maq
