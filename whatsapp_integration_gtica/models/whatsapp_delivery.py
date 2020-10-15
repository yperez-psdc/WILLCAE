# -*- coding: utf-8 -*-

import logging
import urllib
import re

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.http import request

_logger = logging.getLogger(__name__)


class SendWhatsapp(models.TransientModel):
    _name = 'send.whatsapp.stock'
    _description = 'Send Whatsapp'

    partner_id = fields.Many2one('res.partner', domain="[('parent_id','=',partner_id)]")
    default_messege_id = fields.Many2one('whatsapp.template', domain="[('category', '=', 'delivery')]")

    name = fields.Char(related='partner_id.name')
    mobile = fields.Char(related='partner_id.mobile', help="use country mobile code without the + sign")
    format_message = fields.Selection([('txt', 'Text Plan'),
                                       ('link', 'Link Url'),
                                       ], string="Format Message")
    message = fields.Text(string="Message")
    format_visible_context = fields.Boolean(default=False)

    @api.model
    @api.onchange('partner_id')
    def __onchange_partner_id(self):
        self.format_visible_context = self.env.context.get('format_invisible', False)
        self.mobile = self.partner_id.mobile

    @api.onchange('format_message')
    def _onchange_type(self):

        if self.format_message == 'txt' or self.env.context.get('format_invisible'):
            self.message = self.env.context.get('message_txt', False)
        if self.format_message == 'link':
            self.message = self.env.context.get('message_link', False)

    @api.onchange('default_messege_id')
    def _onchange_message(self):
        stock_picking_id = self.env['stock.picking'].browse(self._context.get('active_id'))
        message = self.default_messege_id.template_messege
        incluid_name = ''
        try:
            incluid_name = str(message).format(
                name=stock_picking_id.partner_id.name,
                sales_person=stock_picking_id.user_id.name,
                company=stock_picking_id.company_id.name,
                website=stock_picking_id.company_id.website)
        except Exception:
            raise ValidationError(
                'Quick replies: parameter not allowed in this template, {link_preview} {item_product}')

        if message:
            self.message = incluid_name

    @api.model
    def close_dialog(self):
        return {'type': 'ir.actions.act_window_close'}

    def sending_reset(self):
        stock_picking_id = self.env['stock.picking'].browse(self._context.get('active_id'))
        stock_picking_id.update({
            'send_whatsapp': 'without_sending',
            })
        self.close_dialog()

    def sending_confirmed(self):

        if not self.mobile or not self.message:
            raise ValidationError(_("You must send your WhatsApp message before"))

        stock_picking_id = self.env['stock.picking'].browse(self._context.get('active_id'))
        message_fomat = '<p class="text-info">Successful Whatsapp</p><p><b>Message sent:</b></p>%s' % self.message
        stock_picking_id._action_whatsapp_confirmed(message_fomat.replace('\n', '<br>'))

        stock_picking_id.update({
            'send_whatsapp': 'sent',
            })
        self.close_dialog()

    def sending_error(self):

        if not self.mobile or not self.message:
            raise ValidationError(_("You must send your WhatsApp message before"))

        stock_picking_id = self.env['stock.picking'].browse(self._context.get('active_id'))
        message_fomat = '<p class="text-danger">Error Whatsapp</p><p>The recipient may not have whatsapp / verify the country code / other reasons</p>'
        stock_picking_id._action_whatsapp_confirmed(message_fomat.replace('\n', '<br>'))

        stock_picking_id.update({
            'send_whatsapp': 'not_sent',
            })
        self.close_dialog()

    @api.model
    def send_dialog(self, whatsapp_url):
        action = {'type': 'ir.actions.act_url', 'url': whatsapp_url, 'target': 'new', 'res_id': self.id}

    def send_whatsapp(self):

        if not self.mobile and not self.message:
            raise ValidationError(
                _("You must add the mobile number or message"))
        if not self.mobile and self.message:
            raise ValidationError(_("You must add the mobile number"))
        if self.mobile and not self.message:
            raise ValidationError(_("You must add the message"))

        if self.mobile:
            movil = self.mobile
            array_int = re.findall("\d+", movil)
            whatsapp_number = ''.join(str(e) for e in array_int)

        if self.message:
            messege_prepare = u'{}'.format(self.message)
            messege_encode = urllib.parse.quote(messege_prepare.encode('utf8'))

        mobileRegex = r"android|webos|iphone|ipod|blackberry|iemobile|opera mini"
        user_agent = request.httprequest.environ.get('HTTP_USER_AGENT', '').lower()
        match = re.search(mobileRegex, user_agent)

        if match:
            whatsapp_url = 'https://api.whatsapp.com/send?phone={}&text={}'.format(whatsapp_number, messege_encode)
        else:
            whatsapp_url = 'https://web.whatsapp.com/send?phone={}&text={}'.format(whatsapp_number, messege_encode)

        return {'type': 'ir.actions.act_url',
                'url': whatsapp_url,
                'nodestroy': True,
                'target': 'new',
                'target_type': 'public',
                'res_id': self.id,
                'param': 'whatsapp_action',
                }
