# -*- coding: utf-8 -*-

from odoo import models, fields, api
from num2words import num2words


class StockPicking(models.Model):
    _inherit  = 'stock.picking'

    def _compute_barcode_report(self):
        barcode = ''
        order = self.env['sale.order'].search([('name','=',self.origin)])
        if order:
            employee = self.env['hr.employee'].search([('user_id','=',order.user_id.id)])
            barcode = employee.barcode if employee else ''
        return barcode

    def _compute_box_report(self):
        box = 0 
        if self.state != 'done':
            box = len(self.move_lines.filtered(lambda x: x.product_uom_qty))
        if self.move_line_ids and self.state == 'done':
            box = len(self.move_line_ids)
        number = box
        lang_code = self.partner_id.lang if self.partner_id else 'en_US'
        lang = self.env['res.lang'].with_context(active_test=False).search([('code', '=', lang_code)])
        try:
            word = num2words(number, lang=lang.iso_code).title()
        except NotImplementedError:
            word = num2words(number, lang='en').title()
        return {'box': box, 'word': word}
    
    def _compute_weight_report(self):
        net = 0.0
        gross = 0.0
        if self.state != 'done':
            lines = self.move_lines.filtered(lambda x: x.product_uom_qty)
            net = sum([x.weight for x in lines.product_id])
            # net = sum(lines.product_id.weight)
            gross = sum([x.weight_gross for x in lines.product_id])
            # gross = sum(lines.product_id.weight_gross)
        if self.move_line_ids and self.state == 'done':
            move_line = self.move_line_ids
            net = sum([x.weight for x in move_line.product_id])
            # net = sum(move_line.product_id.weight)
            gross = sum([x.weight_gross for x in move_line.product_id])
            # gross = sum(move_line.product_id.weight_gross)
        return {'net': net, 'gross': gross}
