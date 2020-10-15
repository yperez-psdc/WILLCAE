# -*- coding: utf-8 -*-

import logging
import urllib
import re

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.http import request

_logger = logging.getLogger(__name__)

class SendWhatsappCRM(models.TransientModel):
    _name = 'send.whatsapp.crm'
    _description = 'Send Whatsapp'

    crm_id = fields.Many2one('crm.lead')
    contact_name = fields.Char()
    default_template_id = fields.Many2one('whatsapp.template', domain="[('category', '=', 'crm')]")

    name = fields.Char(related="crm_id.name", required=True,readonly=True)
    type = fields.Selection(related="crm_id.type", )

    mobile = fields.Char(default=False,help="use country mobile code without the + sign")
    broadcast = fields.Boolean(help="Send a message to several of your contacts at once")

    message = fields.Text(string="Message")
    format_visible_context = fields.Boolean(default=False)

    @api.model
    def default_get(self, fields):
        res = super(SendWhatsappCRM, self).default_get(fields)
        active_id = self._context.get('active_id')
        crm_lead = self.env['crm.lead'].browse(active_id)
        mobile = ''

        if crm_lead.type == 'opportunity':
            mobile = crm_lead.partner_id.mobile if crm_lead.partner_id.mobile else crm_lead.partner_id.phone or crm_lead.phone
        if crm_lead.type == 'lead':
            mobile = crm_lead.mobile if crm_lead.mobile else crm_lead.phone

        res.update({
            'crm_id': crm_lead.id,
            'name': crm_lead.name,
            'mobile': mobile,
            'contact_name': crm_lead.partner_id.name if crm_lead.partner_id.name else crm_lead.contact_name,
            })

        return res

    @api.model
    def close_dialog(self):
        return {'type': 'ir.actions.act_window_close'}

    default_template_id = fields.Many2one('whatsapp.template')
    @api.onchange('default_template_id')
    def _onchange_message(self):

        message = self.default_template_id.template_messege
        crm_id = self.crm_id
        incluid_name = ''
        try:
            incluid_name = str(message).format(
                name=self.contact_name,
                sales_person=crm_id.user_id.name,
                company=crm_id.company_id.name,
                website=crm_id.company_id.website)
        except Exception:
            raise ValidationError(
                'Quick replies: parameter not allowed in this template, {link_preview} {item_product}')


        if message:
            self.message = incluid_name

    @api.model
    def send_dialog(self,whatsapp_url):
        action = {'type': 'ir.actions.act_url','url': whatsapp_url,'target': 'new', 'res_id': self.id}

    def sending_reset(self):
        crm_lead_id = self.env['crm.lead'].browse(self._context.get('active_id'))
        crm_lead_id.update({
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

        crm_lead_id = self.env['crm.lead'].browse(self._context.get('active_id'))
        message_fomat = '<p class="text-info">Successful Whatsapp</p><p><b>Message sent:</b></p>%s'% self.message
        crm_lead_id._action_whatsapp_confirmed(message_fomat.replace('\n', '<br>'))

        crm_lead_id.update({
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

        crm_lead_id = self.env['crm.lead'].browse(self._context.get('active_id'))
        message_fomat = '<p class="text-danger">Error Whatsapp</p><p>The recipient may not have whatsapp / verify the country code / other reasons</p>'
        crm_lead_id._action_whatsapp_confirmed(message_fomat.replace('\n', '<br>'))

        crm_lead_id.update({
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
