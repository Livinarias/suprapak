from odoo import models.fields,api

class Helpdesk(models.Model):
    _inherit = 'helpdesk.ticket'

    pqrs = fields.Selection([('print','Print'),('paste','Paste'),('technic','Technic'),('cut','Cut'),('rewind','Rewind')],'PQRS by Product')
    print_id = fields.Many2one('print','Print')
    print = fields.Char()
    paste_id = fields.Many2one('paste','Paste')
    paste = fields.Char()
    technic_id = fields.Many2one('technic','Technic')
    technic = fields.Char()
    cut_id = fields.Many2one('cut','Cut')
    cut = fields.Char()
    rewind_id = fields.Many2one('rewind','Rewind')
    rewind = fields.Char()


class Print(models.Model):
    _name = 'print'
    _description = 'PSRS by Print'

    name = fields.Char('Caused by Print')
    code = field.Char('code')


class Paste(models.Model):
    _name = 'paste'
    _description = 'PSRS by Paste'

    name = fields.Char('Caused by Paste')
    code = field.Char('code')


class Technic(models.Model):
    _name = 'technic'
    _description = 'PSRS by Technic'

    name = fields.Char('Caused by Technic')
    code = field.Char('code')


class Print(models.Model):
    _name = 'rewind'
    _description = 'PSRS by Rewind'

    name = fields.Char('Caused by Rewind')
    code = field.Char('code')


class Cut(models.Model):
    _name = 'cut'
    _description = 'PSRS by Cut'

    name = fields.Char('Caused by Cut')
    code = field.Char('code')