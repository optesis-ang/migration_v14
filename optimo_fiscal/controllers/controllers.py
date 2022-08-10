# -*- coding: utf-8 -*-
from odoo import http

# class OptimoFiscal(http.Controller):
#     @http.route('/optimo_fiscal/optimo_fiscal/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/optimo_fiscal/optimo_fiscal/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('optimo_fiscal.listing', {
#             'root': '/optimo_fiscal/optimo_fiscal',
#             'objects': http.request.env['optimo_fiscal.optimo_fiscal'].search([]),
#         })

#     @http.route('/optimo_fiscal/optimo_fiscal/objects/<model("optimo_fiscal.optimo_fiscal"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('optimo_fiscal.object', {
#             'object': obj
#         })