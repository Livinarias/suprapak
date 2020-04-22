from odoo import fields,models,api

class BudgetTemplate(models.TransientModel):
    _name = 'notification.budget'
    _description = 'This is a wizard to limit Budget'

    def button_send_mail(self):
        self.action_create_activity()
        #self.send_notification()
        return True

    def action_create_activity(self):
        order_id = self.env['pruchase.order'].browse(self._context.get('active_id'))
        model_id = self.env.ref('purchase.model_purchase_order')
        type_id = self.env.ref('mail.mail_activity_data_todo')
        summary = 'El pedido ha sido bloqueado por superar el presupuesto, por favor revisar'
        date_deadline = order_id.validity_date if order_id.validity_date else fields.Date.today()
        for user in order_id.users_ids:
            activity_data = {
                'res_id': order_id.id,
                'res_model_id': model_id.id,
                'activity_type_id': type_id.id,
                'date_deadline': date_deadline,
                'summary': summary,
                'user_id': user.id,
            }
            self.env['mail.activity'].create(activity_data)

    def send_notification(self):
        template_id = self.env.ref('budget_suprapak.mail_template_budget_suprapak').id
        template = self.env['mail.template'].browse(template_id)
        order_id = self.env['purchase.order'].browse(self._context.get('active_id'))
        email_values = {}
        email_values['recipient_ids'] = [(4, partner.id) for partner in order_id.patrners_ids]
        template.send_mail(order_id.id, force_send=True, email_values=email_values)

