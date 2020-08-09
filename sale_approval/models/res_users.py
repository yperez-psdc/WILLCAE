# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, SUPERUSER_ID, _

class Users(models.Model):
    _inherit = "res.users"
    
    sale_order_can_approve = fields.Selection([('yes', 'Yes'), ('no', 'No')], 'Puede Aprobar',default='no')



 


















# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:    