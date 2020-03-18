# -*- coding: utf-8 -*-
# from odoo import http


# class SuprapakMrp(http.Controller):
#     @http.route('/suprapak_mrp/suprapak_mrp/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/suprapak_mrp/suprapak_mrp/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('suprapak_mrp.listing', {
#             'root': '/suprapak_mrp/suprapak_mrp',
#             'objects': http.request.env['suprapak_mrp.suprapak_mrp'].search([]),
#         })

#     @http.route('/suprapak_mrp/suprapak_mrp/objects/<model("suprapak_mrp.suprapak_mrp"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('suprapak_mrp.object', {
#             'object': obj
#         })
