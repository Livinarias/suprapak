from odoo import fields,models,api

class WizardOtif(models.TransientModel):
    _name = 'wizard.otif'

    start_datetime = fields.Datetime('Start Datetime')
    end_datetime = fields.Datetime('End Datetime')