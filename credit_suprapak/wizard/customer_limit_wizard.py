# -*- coding: utf-8 -*-

from odoo import models, fields, api


class customer_limit_wizard(models.TransientModel):
    _inherit = "customer.limit.wizard"
    
    def button_send_mail(self):
        self.set_credit_limit_state()
        self.action_send_mail()
        return True
    
    def action_send_mail(self):
        template_id = self.env.ref('credit_suprapak.mail_template_credit_suprapak').id
        template = self.env['mail.template'].browse(template_id)
        order_id = self.env['sale.order'].browse(self._context.get('active_id'))
        email_values = {}
        email_values['recipient_ids'] = [(4, partner.id) for partner in order_id.patrners_ids]
        # template.email_to = order_id.mail_users
        template.send_mail(order_id.id, force_send=True, email_values=email_values)

        '''self.ensure_one()
        template_id = self.env.ref('credit_suprapak.mail_template_credit_suprapak').id
        lang = self.env.context.get('lang')
        template = self.env['mail.template'].browse(template_id)
        order_id = self.env['sale.order'].browse(self._context.get('active_id'))
        if template.lang:
            lang = template._render_template(template.lang, 'sale.order', order_id.id)
        ctx = {
            'default_model': 'sale.order',
            'default_res_id': order_id.id,
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'custom_layout': "mail.mail_notification_paynow",
            'proforma': order_id.env.context.get('proforma', False),
            'force_email': True,
            'model_description': order_id.with_context(lang=lang).type_name,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }'''

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
