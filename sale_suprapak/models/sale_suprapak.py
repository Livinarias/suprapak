from odoo import models,api,fields

class OtifReport(models.Model):
    _name = 'otif.report'
    _description = "Sales Otif Report"

    country_code = fields.Char('Country Code')
    partner_id = fields.Many2one('res.partner', 'Customer')
    sale_order_id = fields.Many2one('sale.order','Sale Order')
    #kronos fileds
    data_sheet_id = fields.Many2one('data.sheet','Data Sheet')
    customer_code = fields.Char('Customer Code')
    reference_data = fields.Char('Reference')
    material_data = fields.Char('Material')
    #type_order =
    #material_presentation = field.Char('Presentation Material')
    #description = field.Char('Description')
    quantity_requested = field.Char('Quantity Requested')
    unit packing = field.Char('Unit Packing')
    # sale order fields
    commitment_date = fields.Datetime('Commitment Date')
    date_order = fields.Datetime('Date Order')
    lead_time  = fields.Datetime('Lead Time')
    #inventory fields
    #scheduled_date = fields.
    #eta =
    qty_done = fields.Float('Quantity Done')
    #difference_compliance = fields.
    #production fields
    date_planned_start = fields.Datetime('Date Planned Start')
    date_finished = fields.Datetime('Date Finished')





