from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_account_asset = fields.Boolean(string="Activer", implied_group='optimo.group_account_asset')


            