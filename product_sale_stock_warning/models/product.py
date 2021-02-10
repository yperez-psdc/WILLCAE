# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class ResUsers(models.Model):
    _inherit = 'res.users'

    check_no_stock = fields.Boolean(
    	string="Venta Sin Stock",
        help="Permite ver los check para hacer ventas sin stock"
    )

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    custom_check_onhand_qty = fields.Boolean(
    	string="Sales Order Alert",
        help="If qty not in hand at warehouse then raise alert on confirm sales time .",
        compute="_compute_hide"
    )

    hide = fields.Boolean(
        string="Oculto"
    )

    def _compute_hide(self):
        if self.env['res.users'].search([('check_no_stock','=',True)]):
            self.hide = True
        else:
            self.hide = False