from odoo import models,api,fields

class crossoveredBudget(models.Model):
    _inherit = 'purchase.order'

    def validation_budget(self):
        if self.product_id.categ_id.property_account_expense_categ_id in self.general_budget_id:
            if self.general_budget_id.practical_amount > self.general_budget_id.planned_amount:
                wiz_id = self.env['notification.budget']
            else:
                self.action_view_invoice()

