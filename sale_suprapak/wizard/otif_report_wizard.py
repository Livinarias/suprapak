from odoo import fields,models,api
import xlsxwriter
import io
import base64

class OtifReportWizard(models.TransientModel):
    _name = 'otif.report.wizard'
    _description = "Otif report wizard"

    name = fields.Char('File Name', readonly=True)
    data = fields.Binary('File', readonly=True, attachment=False)
    state = fields.Selection([('choose', 'choose'), ('get', 'get')], default='choose')
    start_datetime = fields.Datetime('Start Datetime')
    end_datetime = fields.Datetime('End Datetime')
    attachment_id = fields.Many2one('ir.attachment', 'Attachment')
    data_attachment = fields.Binary(related='attachment_id.datas')

    def generate_file(self):
        this = self[0]

        # Elimina reportes anteriormente creados
        self.env['ir.attachment'].search([('res_model','=','otif.report.wizard')]).unlink()

        # Create an in-memory output file for the new workbook.
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        # Write some test data.
        worksheet.write(0, 0, 'Hello, world!')
        worksheet.write(1, 0, 'Start')
        worksheet.write(1, 1, self.start_datetime)
        worksheet.write(2, 0, 'End')
        worksheet.write(2, 1, self.end_datetime)

        # Orden, Cliente,
        worksheet.write(4, 0, 'Orden')
        worksheet.write(4, 1, 'Cliente')

        # Variables
        domain = [('expected_date','>=',self.start_datetime),('expected_date','<=',self.end_datetime)]
        orders = self.env['sale.order'].search(domain)
        for i, order in enumerate(orders):
            worksheet.write(i + 5, 0, order.name)
            worksheet.write(i + 5, 1, order.partner_id.name)

        # Close the workbook before streaming the data.
        workbook.close()

        # Rewind the buffer.
        output.seek(0)

        # Create attachement
        dic = {
            'name': 'Report.xlsx',
            'type': 'binary',
            'res_model': 'otif.report.wizard',
            'db_datas': base64.encodestring(output.read()),
        }        
        attachment_id = self.env['ir.attachment'].create(dic)

        # return values
        out = base64.encodestring(output.read())
        name = 'Report.xlsx'
        this.write({'state': 'get', 'data': out, 'name': name, 'attachment_id': attachment_id.id})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'otif.report.wizard',
            'view_mode': 'form',
            'res_id': this.id,
            'views': [(False, 'form')],
            'target': 'new',
        }
