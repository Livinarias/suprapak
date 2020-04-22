# -*- coding: utf-8 -*-

from odoo import models, fields, api
import base64


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    signature_request_id = fields.Many2one('sign.request', 'Signature Request', copy=False)
    signature_request_link = fields.Char("Sign link")
    signature_state = fields.Selection(related='signature_request_id.state')
    contract_document = fields.Binary("Signed Document", copy=False)
    contract_document_filename = fields.Char('Signed Filename', copy=False)
    state = fields.Selection(
        [('draft', 'Draft'), ('posted', 'Validated'), ('pdf_sent', 'PDF sent'), ('signed', 'Fully Signed'), ('sent', 'Sent'), ('reconciled', 'Reconciled'),
         ('cancelled', 'Cancelled')], readonly=True, default='draft', copy=False, string="Status")

    def action_email_contract(self):
        for payment in self:
            if not payment.signature_request_id:
                pdf = self.env.ref(
                    'account.action_report_payment_receipt').render_qweb_pdf(payment.id)
                b64_pdf = base64.b64encode(pdf[0])

                # save pdf as attachment
                payment_name = payment and payment.name or payment.partner_id.name
                attachment_name = payment_name + " Not Signed Contract"
                attachment = self.env['ir.attachment'].create({
                    'name': attachment_name,
                    'type': 'binary',
                    'datas': b64_pdf,
                    'res_name': attachment_name + '.pdf',
                    'store_fname': attachment_name,
                    'res_model': self._name,
                    'res_id': payment.id,
                    'mimetype': 'application/x-pdf'
                })

                role_id = self.env.ref('sign.sign_item_role_customer').id
                signature_item_type_id = self.env.ref('sign.sign_item_type_signature')
                template_id = self.env['sign.template'].create({
                    'attachment_id': attachment.id,
                    'sign_item_ids': [(0, 0, {
                        'type_id': signature_item_type_id.id,
                        'required': True,
                        'responsible_id': role_id,
                        'page': 1,
                        'posX': 0.700,
                        'posY': 0.800,
                        'width': 0.200,
                        'height': 0.050
                    })]
                })

                request_id = self.env['sign.request'].create({
                    'reference': payment_name + " Contract",
                    'template_id': template_id.id,
                    'request_item_ids': [
                        (0, 0, {'partner_id': payment.partner_id.id, 'role_id': role_id, 'state': 'draft'})]
                })
                payment.signature_request_id = request_id

            ir_model_data = self.env['ir.model.data']
            try:
                template_id = ir_model_data.get_object_reference('payment_signature_mp',
                                                                 'payment_signature_website_sign_mail_template')[1]
                mail_template = self.env['mail.template'].browse(template_id)
                email_from_usr = self.create_uid.partner_id.name
                email_from_mail = self.create_uid.partner_id.email
                email_from = "%(email_from_usr)s <%(email_from_mail)s>" % {'email_from_usr': email_from_usr,
                                                                           'email_from_mail': email_from_mail}
                message = ""

            except ValueError:
                template_id = False
            try:
                compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
            except ValueError:
                compose_form_id = False

            res = {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'mail.compose.message',
                'views': [(compose_form_id, 'form')],
                'view_id': compose_form_id,
                'target': 'new',
                'context': {
                    'default_model': 'account.payment',
                    'default_res_id': payment.id,
                    'default_use_template': bool(mail_template),
                    'default_template_id': mail_template.id,
                    'default_composition_mode': 'comment',
                    'force_email': True,
                    'lang': payment.partner_id.lang,
                    'template_type': 'request',
                    'email_from_usr': email_from_usr,
                    'email_from_mail': email_from_mail,
                    'email_from': email_from,
                    'email_to': payment.partner_id.email,
                    'link': "sign/document/%(request_id)s/%(access_token)s" % {
                        'request_id': payment.signature_request_id.id,
                        'access_token': payment.signature_request_id.request_item_ids[0].access_token},
                    'subject': "Signature request - " + payment.signature_request_id.display_name,
                    'msgbody': (message or "").replace("\n", "<br/>"),
                    'account_payment_esign_contract': True
                },
            }
            return res
