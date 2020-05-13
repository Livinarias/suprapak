from odoo import models, fields, api

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    kronos_id = fields.Many2one('data.sheet',compute = '_bom_id')

    @api.depends('bom_id')
    def _bom_id(self):
        if self.bom_id:
            self.kronos_id = self.bom_id.sheet_id
        else:
            self.kronos_id = None

    """kronos = fields.Char('Ficha en Kronos',readonly=True,compute = '_bom_id')

    @api.depends('bom_id')
    def _bom_id(self):
        if self.bom_id:
            self.kronos = self.bom_id.sheet_id.name
        else:
            self.kronos =  None"""



