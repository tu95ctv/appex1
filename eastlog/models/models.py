# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, tools
import datetime
from odoo.exceptions import UserError
from odoo.http import request
import time
import base64

class Partner(models.Model):
    _inherit = "res.partner"
    customer = fields.Boolean(string='Is a Customer', default=False,
                               help="Check this box if this contact is a customer.")
    
class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'
    licensecertificate_ids = fields.One2many('eastlog.licensecertificate', 'vehicle_id')
    
        
class LicenseCertificate(models.Model):
    _name = 'eastlog.licensecertificate'
    _description = 'License Certificate'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    vehicle_id = fields.Many2one('fleet.vehicle', required=True)
    name = fields.Char(compute='_name_compute', store=True)
    description = fields.Text(required=True)
    last_registration_date = fields.Date(default=fields.Date.context_today)
#     def offset_date(self):
#         today = datetime.date.today()
#         print ('today',today,type(today))
#         the_day = today + datetime.timedelta(days=-7)
#         return the_day
    expiration_date = fields.Date(default=fields.Date.context_today,required = True)
    is_expire = fields.Boolean('Expire', compute ='_is_expire_compute', store=True )
    resend_mail =  fields.Boolean(help='Resend mail when license expire')
#     body_html = fields.Html()
   
    @api.depends('expiration_date')
    def _is_expire_compute(self):
        for r in self:
            is_expire = fields.Date.from_string(r.expiration_date) < fields.Date.from_string(fields.Date.context_today(self))
            r.is_expire = is_expire
   
#     @api.onchange('expiration_date')
#     def _is_expire_onchange(self):
#         if self.expiration_date:
#             is_expire = fields.Date.from_string(self.expiration_date) < fields.Date.from_string(fields.Date.context_today(self))
#             self.is_expire = is_expire
            
    def check_expire_and_send_mail(self):
        licenses = self.search(['|', ('is_expire', '=', False), ('resend_mail', '=', True)])
        for r in licenses:
            print ('***check_expire_and_send_mail for***',r.name)
            expiration_date = fields.Date.from_string(r.expiration_date)
            is_expire = expiration_date < fields.Date.from_string(fields.Date.context_today(self))
#             if is_expire and not old_is_expire:
            if is_expire:
                if r.is_expire == False:
                    r.is_expire = is_expire
                r.send_mail_to_admin()
                r.resend_mail = False
    def set_is_expire_false(self):
        self.is_expire = False
            
    @api.depends('description','vehicle_id')
    def _name_compute(self):
        for r in self:
            r.name  = '%s-%s'%(r.vehicle_id.name, r.description)
    def create_activity(self, assign_to, str_todo):
        activity_data = {
            'activity_type_id': 4,
            'summary': _(u'%s, Waiting for %s to %s') % (self.name, assign_to.name, str_todo),
            'user_id': assign_to.id,
            'res_id': self.id,
            'res_model_id': self.env['ir.model']._get(self._name).id
        }
        self.env['mail.activity'].create(activity_data)
        
      
  
    def send_mail_to_admin(self):
        template_browse = self.env.ref('eastlog.license_certificate')
        admin_groups = self.env.ref('base.group_erp_manager')
        admins_ids = admin_groups.users
#         if not admins_ids:
#             raise UserError('No admin')
        license_table_email_template = self.env.ref('eastlog.license_table_email')
        values_render  = {
                'doc': self
            }
        body_html = license_table_email_template.render(values_render, 'ir.qweb')
#         raise UserError(license_table)
#         self.body_html = license_table
#         body_html_template = \
#         '''<div style="font-family: 'Lucida Grande', Ubuntu, Arial, Verdana, sans-serif; font-size: 12px; color: rgb(34, 34, 34); background-color: #FFF; ">
#                 <p>Dear Admin!</p>
#                 <p>This is notification expired license</p>
#                 </div>
#                 %{0}
#         '''
#         body_html = body_html_template.format(body_html)
#         body_html = tools.append_content_to_html(body_html, self.env.user.signature, plaintext=False)
#         body_html = tools.html_sanitize(body_html)
        values = {
#             'email_to':admins
            'body':body_html,
            'body_html':body_html,
            'email_to':False,
            'partner_ids':admins_ids.mapped('partner_id.id')
            }
        if self.is_expire:
            for admin in admins_ids:
                self.create_activity(admin, 'Extend Expire')
        self.send_mail(template_browse, self.id, force_send=True, email_values=values)
   
    @api.multi
    def send_mail(self, template_id, res_id, force_send=False, raise_exception=False, email_values=None):
        """Generates a new mail message for the given template and record,
           and schedules it for delivery through the ``mail`` module's scheduler.

           :param int res_id: id of the record to render the template with
                              (model is taken from the template)
           :param bool force_send: if True, the generated mail.message is
                immediately sent after being created, as if the scheduler
                was executed for this message only.
           :param dict email_values: if set, the generated mail.message is
                updated with given values dict
           :returns: id of the mail.message that was created
        """
        self.ensure_one()
        Mail = self.env['mail.mail']
        Attachment = self.env['ir.attachment']  # TDE FIXME: should remove dfeault_type from context
        # create a mail_mail based on values, without attachments
        values = template_id.generate_email(res_id)
        values.update(email_values or {})
        values['recipient_ids'] = [(4, pid) for pid in values.get('partner_ids', list())]
        attachment_ids = values.pop('attachment_ids', [])
        attachments = values.pop('attachments', [])
        # add a protection against void email_from
        if 'email_from' in values and not values.get('email_from'):
            values.pop('email_from')
        mail = Mail.create(values)

        # manage attachments
        for attachment in attachments:
            attachment_data = {
                'name': attachment[0],
                'datas_fname': attachment[0],
                'datas': attachment[1],
                'type': 'binary',
                'res_model': 'mail.message',
                'res_id': mail.mail_message_id.id,
            }
            attachment_ids.append(Attachment.create(attachment_data).id)
        if attachment_ids:
            values['attachment_ids'] = [(6, 0, attachment_ids)]
            mail.write({'attachment_ids': [(6, 0, attachment_ids)]})

        if force_send:
            mail.send(raise_exception=raise_exception)
        return mail.id  # TDE CLEANME: return mail + api.returns ?