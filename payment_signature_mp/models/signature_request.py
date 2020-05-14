# -*- coding: utf-8 -*-

from odoo import fields, api, models


class SignRequest(models.Model):
    _inherit = "sign.request"

    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company)

    def action_signed(self):
        res = super(SignRequest, self).action_signed()
        payment_id = self.env['account.payment'].search([('signature_request_id', '=', self.id)],
                                                        limit=1)
        if payment_id:
            payment_id.contract_document = self.completed_document
            payment_name = payment_id and payment_id.name or payment_id.partner_id.name
            payment_id.state = 'signed'
            payment_id.contract_document_filename = payment_name + ' Signed Payment Report.pdf'
        return res
