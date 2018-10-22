from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError, UserError
from odoo.modules.module import get_module_resource
import re


class Useri(models.Model):
    _name = "user.user"
    _description = "Perdoruesi"
#    _inherit = ['crm.lead','user.user','phone.validation.mixin']


    name = fields.Char(string = "Emri", required = True)
    mbiemri = fields.Char(string="Mbiemri", required=True)
    email = fields.Char(string = "Emaili")
    phone = fields.Char(string = "Numer kontakti")



    # @api.constrains('nr_kontakti')
    # def validate_phoneNumber(self):
    #     b = str(self.nr_kontakti)
    #     c = []
    #     for digit in b:
    #         c.append(int(digit))
    #     gjatesia = len(c)
    #     if gjatesia <10 or gjatesia >10:
    #         raise ValueError("Numri juaj duhet te permbaje 10 shifra")

    # @api.constrains('nr_kontakti')
    # def validate_phoneNumber(self):
    #     if self.nr_kontakti:
    #         match = re.match('^[+0-9]{2,3}+(0-9){10}$',self.nr_kontakti)
    #         if match == None:
    #             raise ValidationError('Not a valid Phone Number')

    @api.constrains('email')
    def validate_mail(self):
        if self.email:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email)
            if match == None:
                raise ValidationError('Not a valid E-mail ID')

    # @api.onchange('phone', 'country_id', 'company_id')
    # def _onchange_phone_validation(self):
    #     if self.phone:
    #         self.phone = self.phone_format(self.phone)
    #
    # @api.onchange('mobile', 'country_id', 'company_id')
    # def _onchange_mobile_validation(self):
    #     if self.mobile:
    #         self.mobile = self.phone_format(self.mobile)