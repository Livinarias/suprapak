from odoo import models,api,fields
from odoo.exceptions import AccessDenied

class AccountMove(models.Model):
    _inherit = 'account.move'

    def validation_budget(self):
        flag = True
        for record in self:
            if record.type == 'in_invoice':
                accounts = record.invoice_line_ids.product_id.categ_id.property_account_expense_categ_id.ids
                for account in accounts:
                    dic = {}
                    dic['date'] = record.date
                    dic['account'] = account
                    domain = [('product_id.categ_id.property_account_expense_categ_id.id','=',account),('move_id.id','=',record.id)]
                    total = 0
                    for line in record.invoice_line_ids.search(domain):
                        total += line.price_subtotal
                    dic['total'] = total
                    flag = self.validate_budget_lines(dic)
        return flag
        '''for lines in self:
            if lines.invoice_line_ids.product_id.categ_id.property_account_expense_categ_id in \
                    lines.crossovered_budget_line.general_budget_id.account_ids:
                if lines.crossovered_budget_line.practical_amount > \
                    lines.crossovered_budget_line.planned_amount:
                    wiz_id = lines.env['notification.budget']
                else:
                    lines.action_post()'''

    def action_post(self):
        if not self.validation_budget():
            # res = self.action_create_activity()
            res = self.action_wizard_budget()
        else:
            res = super(AccountMove, self).action_post()
        return res

    def validate_budget_lines(self, dic):
        # dic = {'date', 'account', 'total'}
        flag = True
        domain = [('crossovered_budget_id.state','=','done'),('date_from','<=',dic['date']),('date_to','>=',dic['date']),
                  ('general_budget_id.account_ids','in',dic['account'])]
        lines = self.env['crossovered.budget.lines'].search(domain)
        for line in lines:
            # if dic['account'] in line.general_budget_id.account_ids.ids:
            if line.theoritical_amount + dic['total'] > line.planned_amount:
                flag = False
        return flag

    def action_create_activity(self):
        for record in self:
            order_id = record
            model_id = self.env.ref('account.model_account_move')
            type_id = self.env.ref('mail.mail_activity_data_todo')
            summary = 'El pedido ha sido bloqueado por superar el presupuesto, por favor revisar'
            date_deadline = record.date if record.date else fields.Date.today()
            partners = record.message_follower_ids.partner_id.ids
            users = self.env['res.users'].search([('partner_id.id', 'in', partners)]).ids
            for user in users:
                activity_data = {
                    'res_id': order_id.id,
                    'res_model_id': model_id.id,
                    'activity_type_id': type_id.id,
                    'date_deadline': date_deadline,
                    'summary': summary,
                    'user_id': user,
                }
                self.env['mail.activity'].create(activity_data)
        return {
                'warning': {
                    'title': "Superó el presupuesto",
                    'message': "Con esta compra supera el presupuesto,por favor comuniquese con la persona encargada del presupuesto",
                    },
                }

    """{
        'men': 'adadasd'
        'users_ids': [(4,ids,0)]
    }"""



