from odoo import models,api,fields

class crossoveredBudget(models.Model):
    _inherit = 'purchase.order'

    def validation_budget(self):
        if self.practical_amount > self.planned_amount:
            wiz_id = self.env['notification.budget']
        else:
            self.action_view_invoice()

