# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT

class SaleOrder(models.Model):
    _inherit = "sale.order"
     
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('pendint', 'Pendiente'),
        ('approve', 'Aprobado'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')
    approver_id = fields.Many2one('res.users', 'Sale Order Approver', readonly=True, copy=False, track_visibility='onchange', default=lambda self: self.env.user)
    
    #@api.multi
    def action_confirm_2(self):
        for sale_order in self:
            if not sale_order.approver_id == self.env.user: 
                raise UserError(_('No tiene permisos para confirmar este presupuesto, contacte a su administrador.'))
        return self.write({'state': 'approve'})

    #@api.multi
    def print_quotation(self):
        self.filtered(lambda s: s.state == 'draft').write({'state': 'sent'})

        return self.env.ref('sale.action_report_saleorder')\
            .with_context(discard_logo_check=True).report_action(self)