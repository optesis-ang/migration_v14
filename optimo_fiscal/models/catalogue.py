# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
class FamilyInherit(models.Model):
    _inherit = "optesis.family"

    num_compte = fields.Char("Compte")
  