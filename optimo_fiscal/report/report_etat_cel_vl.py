# -*- coding:utf-8 -*-
# by ANG
from odoo import api, fields, models, _
class ParticularReport(models.AbstractModel):
    _name = 'optesis.report.etat.cel.vl'
    _description = "Etat cel vel report"
    
    @api.model
    def _get_report_values(self, docids, data=None):
       model = self.env.context.get('active_model')
       docs = self.env[model].browse(self.env.context.get('active_id'))
       #get_periods, months, total_mnths = self.get_periods(data['form'])

       return {
           'doc_ids': docids,
           'doc_model': model,
           'data': data,
           'docs': docs,

       }
    