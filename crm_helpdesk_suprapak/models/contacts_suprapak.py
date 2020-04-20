from odoo import models,api,fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    ticket_count = fields.Integer('Number of Tickets', compute = '_compute_tickets')
    ticket_ids = fields.One2many('helpdesk.ticket','partner_id','Tickets')

    def _compute_tickets(self):
        for ticket in self:
            count = len(ticket.ticket_ids)
            ticket.ticket_count = count

    def action_view_ticket(self):
        action = self.env.ref('crm_helpdesk_suprapak.action_ticket').read()[0]
        action['context'] = {
            'default_partner_id': self.partner_id.id,
            'default_partner_id': self.id
        }
        action['domain'] = [('partner_id', '=', self.id)]
        return action