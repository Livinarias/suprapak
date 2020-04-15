from odoo import models, fields, api

class InvoiceTemplate(models.Model):
    _inherit = 'account.move'

    parent = fields.Char(readonly=True, compute = '_compute_partner_id')

    @api.depends('partner_id')
    def _compute_partner_id(self):
        if self.partner_id:
            self.parent = self.partner_id.parent_id.name
        else:
            self.parent = None
