# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class Users(models.Model):
    _inherit = 'res.users'

    check_no_stock = fields.Boolean(
    	string="Venta Sin Stock",
        help="Permite ver los check para hacer ventas sin stock",
        compute="_compute_hide"
    )

    def _compute_hide(self):
        if self.check_no_stock == True:
            self.env['product.template'].write({'hide':True})
            self.env['sale.order'].write({'hide':True})
        else:
            self.env['product.template'].write({'hide':False})
            self.env['sale.order'].write({'hide':False})

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    custom_check_onhand_qty = fields.Boolean(
    	string="Sales Order Alert",
        help="If qty not in hand at warehouse then raise alert on confirm sales time ."
    )

    hide = fields.Boolean(
        string="Oculto"
    )