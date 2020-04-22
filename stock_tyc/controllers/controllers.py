# -*- coding: utf-8 -*-
# from odoo import http


# class StockTyc(http.Controller):
#     @http.route('/stock_tyc/stock_tyc/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_tyc/stock_tyc/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_tyc.listing', {
#             'root': '/stock_tyc/stock_tyc',
#             'objects': http.request.env['stock_tyc.stock_tyc'].search([]),
#         })

#     @http.route('/stock_tyc/stock_tyc/objects/<model("stock_tyc.stock_tyc"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_tyc.object', {
#             'object': obj
#         })
