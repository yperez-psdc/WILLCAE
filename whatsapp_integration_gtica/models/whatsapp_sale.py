# -*- coding: utf-8 -*-

import logging
import urllib
import re
import html2text

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.http import request

_logger = logging.getLogger(__name__)

class ConvertHtmlText(object):

    def convert_html_to_text(result_txt):
        capt = b'%s' % (result_txt)
        convert_byte_to_str = capt.decode('utf-8')
        return html2text.html2text(convert_byte_to_str)


class SendWhatsapp(models.TransientModel):
    _name = 'send.whatsapp.sale'
    _description = 'Send Whatsapp Sale'

    partner_id = fields.Many2one('res.partner', domain="[('parent_id','=',partner_id)]")
    default_messege_id = fields.Many2one('whatsapp.template', domain="['|', ('category', '=', 'sale'), ('category', '=', 'provider')]")

    name = fields.Char(related='partner_id.name',required=True,readonly=True)
    mobile = fields.Char(related='partner_id.mobile',help="use country mobile code without the + sign")
    broadcast = fields.Boolean(help="Send a message to several of your contacts at once")
    format_message = fields.Selection([('txt', 'Text Plan'),
                                 ('link', 'Link Url'),
                                  ], string="Format Message")
    message = fields.Text(string="Message")
    format_visible_context = fields.Boolean(default=False)

    @api.model
    @api.onchange('partner_id')
    def _onchange_partner_id(self):
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
        sale_order_id = self.env['sale.order'].browse(self._context.get('active_id'))
        message = self.default_messege_id.template_messege
        url_preview = sale_order_id.url_link_sale()
        items_products = ConvertHtmlText.convert_html_to_text(sale_order_id.items_products())
        
        try:
            incluid_name = str(message).format(
                name=sale_order_id.partner_id.name,
                sales_person=sale_order_id.user_id.name,
                company=sale_order_id.company_id.name,
                website=sale_order_id.company_id.website,
                link_preview=url_preview,
                item_product=items_products, )
        except Exception:
            raise ValidationError('Quick replies: parameter not allowed in this template')

        if message:
            self.message = incluid_name


    @api.model
    def close_dialog(self):
        return {'type': 'ir.actions.act_window_close'}

    @api.model
    def send_dialog(self,whatsapp_url):
        action = {'type': 'ir.actions.act_url','url': whatsapp_url,'target': 'new', 'res_id': self.id}

    def sending_reset(self):
        sale_order_id = self.env['sale.order'].browse(self._context.get('active_id'))
        sale_order_id.update({
            'send_whatsapp': 'without_sending',
            })
        self.close_dialog()

    def sending_confirmed(self):

        if not self.mobile and not self.message and not self.broadcast:
            raise ValidationError(_("You must add the mobile number or message (You can use the broadcast list option)"))
        if not self.mobile and self.message and not self.broadcast:
            raise ValidationError(_("You must add the mobile number (You can use the broadcast list option)"))
        if not self.mobile and not self.message and self.broadcast:
            raise ValidationError(_("You must add the message"))
        if self.mobile and not self.message and not self.broadcast:
            raise ValidationError(_("You must add the message"))
        if self.mobile and not self.message and self.broadcast:
            raise ValidationError(_("You must add the message"))

        sale_order_id = self.env['sale.order'].browse(self._context.get('active_id'))
        message_fomat = '<p class="text-info">Successful Whatsapp</p><p><b>Message sent:</b></p>%s'% self.message
        sale_order_id._action_whatsapp_confirmed(message_fomat.replace('\n', '<br>'))
        sale_order_id.update({
            'send_whatsapp': 'sent',
            })
        self.close_dialog()

    def sending_error(self):

        if not self.mobile and not self.message and not self.broadcast:
            raise ValidationError(_("You must add the mobile number or message (You can use the broadcast list option)"))
        if not self.mobile and self.message and not self.broadcast:
            raise ValidationError(_("You must add the mobile number (You can use the broadcast list option)"))
        if not self.mobile and not self.message and self.broadcast:
            raise ValidationError(_("You must add the message"))
        if self.mobile and not self.message and not self.broadcast:
            raise ValidationError(_("You must add the message"))
        if self.mobile and not self.message and self.broadcast:
            raise ValidationError(_("You must add the message"))

        sale_order_id = self.env['sale.order'].browse(self._context.get('active_id'))
        message_fomat = '<p class="text-danger">Error Whatsapp</p><p>The recipient may not have whatsapp / verify the country code / other reasons</p>'
        sale_order_id._action_whatsapp_confirmed(message_fomat.replace('\n', '<br>'))
        sale_order_id.update({
            'send_whatsapp': 'not_sent',
            })
        self.close_dialog()

    def send_whatsapp(self):

        if not self.mobile and not self.message and not self.broadcast:
            raise ValidationError(_("You must add the mobile number or message (You can use the broadcast list option)"))
        if not self.mobile and self.message and not self.broadcast:
            raise ValidationError(_("You must add the mobile number (You can use the broadcast list option)"))
        if not self.mobile and not self.message and self.broadcast:
            raise ValidationError(_("You must add the message"))
        if self.mobile and not self.message and not self.broadcast:
            raise ValidationError(_("You must add the message"))
        if self.mobile and not self.message and self.broadcast:
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

        if self.broadcast:
            if match:
                whatsapp_url = 'https://api.whatsapp.com/send?text={}'.format(messege_encode)
            else:
                whatsapp_url = 'https://web.whatsapp.com/send?text={}'.format(messege_encode)
        else:
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
