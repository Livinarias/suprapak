from odoo import fields,models,api

class BudgetTemplate(models.TransientModel):
    _name = 'notification.budget'
    _description = 'This is a wizard to limit Budget'

    def button_send_mail(self):
        self.send_notification()
        return True

    def send_notification(self):
        template_id = self.env.ref('budget_suprapak.mail_template_budget_suprapak').id
        template = self.env['mail.template'].browse(template_id)
        order_id = self.env['purchase.order'].browse(self._context.get('active_id'))
        email_values = {}
        email_values['recipient_ids'] = [(4, partner.id) for partner in order_id.patrners_ids]
        template.send_mail(order_id.id, force_send=True, email_values=email_values)

