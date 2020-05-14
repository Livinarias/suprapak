# -*- coding: utf-8 -*-

from odoo import api, models


class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    def send_mail(self, auto_commit=False):
        context = self._context

        if context.get('default_model') == 'account.payment' and context.get('default_res_id') and context.get(
            'account_payment_esign_contract'):
            payment_id = self.env['account.payment'].browse(context['default_res_id'])
            # if payment_id.signature_request_id.state != 'sent':
            # payment_id.signature_request_id.write({'state': 'sent'})
            payment_id.signature_request_id.request_item_ids[0].action_sent()
            payment_id.state = 'pdf_sent'
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            payment_id.signature_request_link = base_url + "/sign/document/%(request_id)s/%(access_token)s" % {
                'request_id': payment_id.signature_request_id.id,
                'access_token': payment_id.signature_request_id.request_item_ids[0].access_token}

        return super(MailComposeMessage, self).send_mail(auto_commit=auto_commit)
