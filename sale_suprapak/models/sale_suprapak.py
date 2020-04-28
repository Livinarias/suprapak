from odoo import models,api,fields

class OtifReport(models.Model):
    _name = 'otif.report'
    _description = "Sales Otif Report"

    country_code = fields.Char('Country Code',readonly=True)
    partner_id = fields.Many2one('res.partner','Customer',readonly=True)
    sale_order_id = fields.Many2one('sale.order','Sale Order',readonly=True)
    #kronos fileds
    data_sheet_id = fields.Many2one('data.sheet','Data Sheet',readonly=True)
    customer_code = fields.Char('Customer Code',readonly=True)
    reference_data = fields.Char('Reference',readonly=True)
    material_data = fields.Char('Material',readonly=True)
    #type_order =
    #material_presentation = field.Char('Presentation Material',readonly=True)
    #description = field.Char('Description',readonly=True)
    quantity_requested = fields.Char('Quantity Requested',readonly=True)
    unit_packing = fields.Char('Unit Packing',readonly=True)
    # sale order fields
    commitment_date = fields.Datetime('Commitment Date',readonly=True)
    date_order = fields.Datetime('Date Order',readonly=True)
    lead_time  = fields.Datetime('Lead Time',readonly=True)
    #inventory fields
    #scheduled_date = fields.
    #eta =
    qty_done = fields.Float('Quantity Done',readonly=True)
    #difference_compliance = fields.
    transporter = fields.Many2one('Transporter',readonly=True)
    num_transporter = fields.Char('Transporter Guide',readonly=True)
    #production fields
    date_planned_start = fields.Datetime('Date Planned Start',readonly=True)
    date_finished = fields.Datetime('Date Finished',readonly=True)
    quality_PDN = fields.Float('Quality PDN',readonly=True)
    PDN_delay = fields.Datetime('PDN Delay',readonly=True)
    #invoice
    sale_invoice = fields.Char('Invoice Order',readonly=True)


class ResCountry(models.Model):
    _inherit = 'res.country.state'

    number_code = fields.Integer('Number Code')

    _sql_constraints = [
        ('name_number_code_uniq', 'unique(country_id,number_code)', 'The code of the state must be unique by country !')
    ]




