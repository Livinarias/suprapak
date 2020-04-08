# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit  = 'product.template'

    x_currency_id = fields.Many2one('res.currency', 'Currency')
    customer_reference = fields.Char('Customer Reference')
    date_version = fields.Date('Date Version')
    class_print = fields.Char('Class of Print')
    presentation = fields.Char('Presentation')
    type_selle = fields.Char('Type of Sealed')
    tipo_producto = fields.Selection([('terminado','Producto terminado'),('materia','Materia Prima')],'Tipo de Producto',required=True)

class ProductProduct(models.Model):
    _inherit  = 'product.product'

    x_currency_id = fields.Many2one('res.currency', 'Currency')
    customer_reference = fields.Char('Customer Reference')
    date_version = fields.Date('Date Version')
    class_print = fields.Char('Class of Print')
    presentation = fields.Char('Presentation')
    type_selle = fields.Char('Type of Sealed')
    tipo_producto = fields.Selection([('terminado','Producto terminado'),('materia','Materia Prima')],'Tipo de Producto',required=True)
