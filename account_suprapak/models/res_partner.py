from odoo import models, fields, api

class InvoiceTemplate(models.Model):
    _inherit = 'res.partner'

    # parent = fields.Char(readonly=True, compute = '_compute_partner_id')
    bool_parent = fields.Boolean('Parent', default=False)

    '''@api.depends('partner_id')
    def _compute_partner_id(self):
        if self.partner_id:
            self.parent = self.partner_id.parent_id.name
        else:
            self.parent = None'''
