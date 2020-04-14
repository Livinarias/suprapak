from odoo import models, fields, api

class InvoiceTemplate(models.Model):
    _inherit = 'account.move'
