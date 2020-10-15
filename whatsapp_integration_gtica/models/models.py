# -*- coding: utf-8 -*-

import logging
import urllib
import html2text
from odoo import http, models, fields, api, tools, _
from odoo.http import request

_logger = logging.getLogger(__name__)

class ConvertHtmlText(object):

    def convert_html_to_text(result_txt):
        capt = b'%s' % (result_txt)
        convert_byte_to_str = capt.decode('utf-8')
        return html2text.html2text(convert_byte_to_str)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    send_whatsapp = fields.Selection([
        ('without_sending', 'without sending'),
        ('sent', 'sent'), ('not_sent', 'no sent'),
        ], default='without_sending')

    def items_products(self):
        record = self.with_context(proforma=True)
        data = request.env['ir.ui.view'].render_template("whatsapp_integration_gtica.template_products_sale", {
            'doc_ids': self.ids,
            'doc_model': 'sale.order',
            'docs': record,
        })

        return data

    def url_link_sale(self):

        dominio = http.request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        url_preview = self.get_portal_url()
        format_url = '{}{}'.format(dominio, url_preview)

        return format_url


    def send_whatsapp_step(self):

        record = self.with_context(proforma=True)
        dominio = http.request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        url_preview = self.get_portal_url()
        format_url = '{}{}'.format(dominio, url_preview)

        result_txt = request.env['ir.ui.view'].render_template("whatsapp_integration_gtica.template_quote", {
            'doc_ids': self.ids,
            'doc_model': 'sale.order',
            'docs': record,
        })
        result_link = request.env['ir.ui.view'].render_template("whatsapp_integration_gtica.template_quote_link", {
            'doc_ids': self.ids,
            'doc_model': 'sale.order',
            'docs': record,
        })

        message_txt = ConvertHtmlText.convert_html_to_text(result_txt)
        message_link = ConvertHtmlText.convert_html_to_text(result_link)
        message_with_link = str(message_link).format(link =format_url)

        return {'type': 'ir.actions.act_window',
                'name': _('Send Whatsapp'),
                'res_model': 'send.whatsapp.sale',
                'target': 'new',
                'view_mode': 'form',
                'view_type': 'form',
                'context': {'default_partner_id': self.partner_id.id, 'message_txt': message_txt, 'message_link': message_with_link},
                }

    def _action_whatsapp_confirmed(self, message=None):
        self.ensure_one()
        lang = self.env.context.get('lang')

        ctx = {
            'default_model': 'sale.order',
            'default_res_id': self.ids[0],
            'default_composition_mode': 'comment',
            'mark_so_as_sent': False,
            'mark_whatsapp_sent': True,
            'custom_layout': False,
            'proforma': self.env.context.get('proforma', False),
            'force_email': False,
            'model_description': self.with_context(lang=lang).type_name,
            }
        self.with_context(ctx).message_post(attachment_ids=[], body=message, canned_response_ids=[], channel_ids=[], message_type='notification', partner_ids=[], subtype='mail.mt_note')

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, **kwargs):

        res = super(SaleOrder, self.with_context(mail_post_autofollow=True)).message_post(**kwargs)
        if self.env.context.get('mark_whatsapp_sent'):
           pass

        return res


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    send_whatsapp = fields.Selection([
        ('without_sending', 'without sending'),
        ('sent', 'sent'), ('not_sent', 'no sent'),
        ], default='without_sending')

    def send_whatsapp_step(self):

        record = self.with_context(proforma=True)
        dominio = http.request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        url_preview = self.get_portal_url()
        format_url = '{}{}'.format(dominio, url_preview)

        result_txt = request.env['ir.ui.view'].render_template("whatsapp_integration_gtica.template_purchase", {
            'doc_ids': self.ids,
            'doc_model': 'purchase.order',
            'docs': record,
        })
        result_link = request.env['ir.ui.view'].render_template("whatsapp_integration_gtica.template_purchase_link", {
            'doc_ids': self.ids,
            'doc_model': 'purchase.order',
            'docs': record,
        })

        message_txt = ConvertHtmlText.convert_html_to_text(result_txt)
        message_link = ConvertHtmlText.convert_html_to_text(result_link)
        message_with_link = str(message_link).format(link =format_url)

        return {'type': 'ir.actions.act_window',
                'name': _('Send Whatsapp'),
                'res_model': 'send.whatsapp.purchase',
                'target': 'new',
                'view_mode': 'form',
                'view_type': 'form',
                'context': {'default_partner_id': self.partner_id.id, 'message_txt': message_txt, 'message_link': message_with_link},
                }

    def _action_whatsapp_confirmed(self, message=None):
        self.ensure_one()
        lang = self.env.context.get('lang')

        ctx = {
            'default_model': 'purchase.order',
            'default_res_id': self.ids[0],
            'default_composition_mode': 'comment',
            'mark_so_as_sent': False,
            'mark_whatsapp_sent': True,
            'custom_layout': False,
            'proforma': self.env.context.get('proforma', False),
            'force_email': False,
            }
        self.with_context(ctx).message_post(attachment_ids=[], body=message, canned_response_ids=[], channel_ids=[], message_type='notification', partner_ids=[], subtype='mail.mt_note')

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, **kwargs):

        res = super(PurchaseOrder, self.with_context(mail_post_autofollow=True)).message_post(**kwargs)
        if self.env.context.get('mark_whatsapp_sent'):
           pass

        return res

class AccountInvoice(models.Model):
    _inherit = 'account.move'

    def items_products(self):
        record = self.with_context(proforma=True)
        data = request.env['ir.ui.view'].render_template("whatsapp_integration_gtica.template_products_invoice", {
            'doc_ids': self.ids,
            'doc_model': 'account.invoice',
            'docs': record,
        })

        return data

    def url_link_invoice(self):

        dominio = http.request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        url_preview = self.get_portal_url()
        format_url = '{}{}'.format(dominio, url_preview)

        return format_url

    send_whatsapp = fields.Selection([
        ('without_sending', 'without sending'),
        ('sent', 'sent'), ('not_sent', 'no sent'),
        ], default='without_sending')

    def send_whatsapp_step(self):

        record = self.with_context(proforma=True)
        dominio = http.request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        url_preview = self.get_portal_url()
        format_url = '{}{}'.format(dominio, url_preview)

        result_txt = request.env['ir.ui.view'].render_template("whatsapp_integration_gtica.template_invoice", {
            'doc_ids': self.ids,
            'doc_model': 'account.move',
            'docs': record,
        })
        result_link = request.env['ir.ui.view'].render_template("whatsapp_integration_gtica.template_invoice_link", {
            'doc_ids': self.ids,
            'doc_model': 'account.move',
            'docs': record,
        })

        message_txt = ConvertHtmlText.convert_html_to_text(result_txt)
        message_link = ConvertHtmlText.convert_html_to_text(result_link)
        message_with_link = str(message_link).format(link =format_url)

        return {'type': 'ir.actions.act_window',
                'name': _('Send Whatsapp'),
                'res_model': 'send.whatsapp.invoice',
                'target': 'new',
                'view_mode': 'form',
                'view_type': 'form',
                'context': {'default_partner_id': self.partner_id.id, 'message_txt': message_txt, 'message_link': message_with_link},
                }

    def _action_whatsapp_confirmed(self, message=None):
        self.ensure_one()
        lang = self.env.context.get('lang')

        ctx = {
            'default_model': 'account.move',
            'default_res_id': self.ids[0],
            'default_composition_mode': 'comment',
            'mark_so_as_sent': False,
            'mark_whatsapp_sent': True,
            'force_email': False,
            }
        self.with_context(ctx).message_post(attachment_ids=[], body=message, canned_response_ids=[], channel_ids=[], message_type='notification', partner_ids=[], subtype='mail.mt_note')

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, **kwargs):

        res = super(AccountInvoice, self.with_context(mail_post_autofollow=True)).message_post(**kwargs)
        if self.env.context.get('mark_whatsapp_sent'):
           pass

        return res

class Lead(models.Model):
    _inherit = 'crm.lead'

    send_whatsapp = fields.Selection([
        ('without_sending', 'without sending'),
        ('sent', 'sent'), ('not_sent', 'no sent'),
    ], default='without_sending')

    def send_whatsapp_step(self):

        return {'type': 'ir.actions.act_window',
                'name': _('Send Whatsapp'),
                'res_model': 'send.whatsapp.crm',
                'target': 'new',
                'view_mode': 'form',
                'view_type': 'form',
                'context': {},
                }

    def _action_whatsapp_confirmed(self, message=None):
        self.ensure_one()
        lang = self.env.context.get('lang')

        ctx = {
            'default_model': 'crm.lead',
            'default_res_id': self.ids[0],
            'default_composition_mode': 'comment',
            'mark_so_as_sent': False,
            'mark_whatsapp_sent': True,
            'force_email': False,
            }

        self.with_context(ctx).message_post(attachment_ids=[], body=message, canned_response_ids=[], channel_ids=[],
                                            message_type='notification', partner_ids=[], subtype='mail.mt_note')

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, **kwargs):

        res = super(Lead, self.with_context(mail_post_autofollow=True)).message_post(**kwargs)
        if self.env.context.get('mark_whatsapp_sent'):
            pass

        return res

class ResPartner(models.Model):
    _inherit = 'res.partner'

    send_whatsapp = fields.Selection([
        ('without_sending', 'without sending'),
        ('sent', 'sent'), ('not_sent', 'no sent'),
        ], default='without_sending')

    def send_whatsapp_step(self):
        return {'type': 'ir.actions.act_window',
                'name': _('Send Whatsapp'),
                'res_model': 'send.whatsapp.partner',
                'target': 'new',
                'view_mode': 'form',
                'view_type': 'form',
                'context': {'default_partner_id': self.id, 'format_invisible': True},
                }

    def _action_whatsapp_confirmed(self, message=None):
        self.ensure_one()
        lang = self.env.context.get('lang')

        ctx = {
            'default_model': 'res.partner',
            'default_res_id': self.ids[0],
            'default_composition_mode': 'comment',
            'mark_so_as_sent': False,
            'mark_whatsapp_sent': True,
            'custom_layout': False,
            'proforma': self.env.context.get('proforma', False),
            'force_email': False,
            }
        self.with_context(ctx).message_post(attachment_ids=[], body=message, canned_response_ids=[], channel_ids=[], message_type='notification', partner_ids=[], subtype='mail.mt_note')

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, **kwargs):

        res = super(ResPartner, self.with_context(mail_post_autofollow=True)).message_post(**kwargs)
        if self.env.context.get('mark_whatsapp_sent'):
           pass

        return res

class StockPickig(models.Model):
    _inherit = 'stock.picking'

    send_whatsapp = fields.Selection([
        ('without_sending', 'without sending'),
        ('sent', 'sent'), ('not_sent', 'no sent'),
        ], default='without_sending')

    def send_whatsapp_step(self):

        record = self.with_context(proforma=True)

        result_txt = request.env['ir.ui.view'].render_template("whatsapp_integration_gtica.template_stock_picking", {
            'doc_ids': self.ids,
            'doc_model': 'stock.picking',
            'docs': record,
        })

        message_txt = ConvertHtmlText.convert_html_to_text(result_txt)

        return {'type': 'ir.actions.act_window',
                'name': _('Send Whatsapp'),
                'res_model': 'send.whatsapp.stock',
                'target': 'new',
                'view_mode': 'form',
                'view_type': 'form',
                'context': {'default_partner_id': self.partner_id.id, 'message_txt': message_txt, 'format_invisible': True},
                }

    def _action_whatsapp_confirmed(self, message=None):
        self.ensure_one()
        lang = self.env.context.get('lang')

        ctx = {
            'default_model': 'stock.picking',
            'default_res_id': self.ids[0],
            'default_composition_mode': 'comment',
            'mark_so_as_sent': False,
            'mark_whatsapp_sent': True,
            'force_email': False,
            }
        self.with_context(ctx).message_post(attachment_ids=[], body=message, canned_response_ids=[], channel_ids=[], message_type='notification', partner_ids=[], subtype='mail.mt_note')

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, **kwargs):

        res = super(StockPickig, self.with_context(mail_post_autofollow=True)).message_post(**kwargs)
        if self.env.context.get('mark_whatsapp_sent'):
           pass

        return res

class account_payment(models.Model):
    _inherit = 'account.payment'

    send_whatsapp = fields.Selection([
        ('without_sending', 'without sending'),
        ('sent', 'sent'), ('not_sent', 'no sent'),
        ], default='without_sending')

    def send_whatsapp_step(self):
        record = self.with_context(proforma=True)
        result_txt = request.env['ir.ui.view'].render_template("whatsapp_integration_gtica.template_payment", {
            'doc_ids': self.ids,
            'doc_model': 'account.payment',
            'docs': record,
            })

        result_link = request.env['ir.ui.view'].render_template(
            "whatsapp_integration_gtica.template_payment_link", {
                'doc_ids': self.ids,
                'doc_model': 'account.payment',
                'docs': record,
                })

        message_txt = ConvertHtmlText.convert_html_to_text(result_txt)
        message_link = ConvertHtmlText.convert_html_to_text(result_link)
        #message_with_link = str(message_link).format(link=format_url)

        return {'type': 'ir.actions.act_window',
                'name': _('Send Whatsapp'),
                'res_model': 'send.whatsapp.payment',
                'target': 'new',
                'view_mode': 'form',
                'view_type': 'form',
                'context': {'default_partner_id': self.partner_id.id, 'message_txt': message_txt,
                            'message_link': message_link},
                }

    def _action_whatsapp_confirmed(self, message=None):
        self.ensure_one()
        lang = self.env.context.get('lang')

        ctx = {
            'default_model': 'account.payment',
            'default_res_id': self.ids[0],
            'default_composition_mode': 'comment',
            'mark_so_as_sent': False,
            'mark_whatsapp_sent': True,
            'force_email': False,
            }
        self.with_context(ctx).message_post(attachment_ids=[], body=message, canned_response_ids=[], channel_ids=[], message_type='notification', partner_ids=[], subtype='mail.mt_note')

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, **kwargs):

        res = super(account_payment, self.with_context(mail_post_autofollow=True)).message_post(**kwargs)
        if self.env.context.get('mark_whatsapp_sent'):
           pass

        return res
