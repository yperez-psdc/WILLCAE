# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class SaleApprovalReason(models.TransientModel):
    _name = 'sale.approval.reason'
    
    notes = fields.Text('Notes')
     
    #@api.multi
    def approve(self):
        sale_br_obj = self.env['sale.order'].browse(self._context.get('active_ids'))[0]
        user_obj = self.env['res.users']
        if self.notes:
            user_search = user_obj.search([('sale_order_can_approve', '=', 'yes')])
            if user_search:
                next_larg_amount_user_id = user_search[0]
                print(next_larg_amount_user_id,'large')
                sale_br_obj.write({'approver_id': next_larg_amount_user_id.id, 'state': 'pendint'})
        ctx = self.env.context.copy()
        ctx.update({'discount_notes': str(self.notes)})
        sale_br_obj.with_context(ctx)
        return True
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
