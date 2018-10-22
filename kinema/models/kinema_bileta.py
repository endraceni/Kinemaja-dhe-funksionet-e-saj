from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError, UserError
from odoo.modules.module import get_module_resource
import datetime


class Salla (models.Model):
        _name = "salla.salla"
        _description = "Informacion mbi sallat"

        name = fields.Char(string = "Emri Salles", required = True)
        kapaciteti = fields.Integer(string = "Kapaciteti", required = True)
        info_shtese = fields.Text(string = "Informacion Shtese")
        state = fields.Selection([('e lire', 'e Lire'), ('e zene', 'e Zene')], default="e lire", string="State")


class Shfaqje(models.Model):
        _name = "shfaqje.filmi"
        _description = "Informacion mbi shfaqjen"

        name = fields.Char(string="Titulli i shfaqjes", required=True, ondelete="cascade")
        id_salla = fields.Many2one('salla.salla', string="Salla")
        id_film = fields.Many2one('film.film', string="Filmi")
        ora_fillimit = fields.Datetime(string="Orari Fillimit", required=True)
        ora_perfundimit = fields.Datetime(string="Orari perfundimit", required=True)
        state = fields.Selection([('aktive', 'Aktive'), ('draft', 'Draft'), ('anulluar', 'Anulluar'), ('perfunduar', 'Perfunduar')],default="draft", string="State")
        bileta_id = fields.One2many('bileta.bileta', 'shfaqje_id', string="Bileta")


        # Gjenero Bileta
        @api.multi
        def gjenero_bileta(self):
            for shfaqje in self:
                if shfaqje.id_salla:
                    if shfaqje.id_salla.kapaciteti:
                        for r in range(0, shfaqje.id_salla.kapaciteti):
                            self.env['bileta.bileta'].create({'serial_no': r, 'shfaqje_id': shfaqje.id})

        @api.multi
        def cancel_show(self):
            for shfaqje in self:
                if shfaqje.id_salla.kapaciteti:
                    self.env['bileta.bileta'].search(
                        ['&', ('shfaqje_id', '=', shfaqje.id), ('state', '!=', 'konfirmuar')]).unlink()

        @api.one
        def draft(self):
            self.state = 'draft'
            self.id_salla.state = 'e zene'

        @api.one
        def aktive(self):
            self.state = 'aktive'
            self.gjenero_bileta()

        @api.one
        def anulluar(self):
            self.state = 'anulluar'
            self.cancel_show()

        @api.one
        def perfunduar(self):
            self.state = 'perfunduar'
            for bileta in self:
                if bileta.bileta_id:
                    self.bileta_id.write({'state': 'perfunduar'})

class Bileta(models.Model):
        _name = "bileta.bileta"
        _description = "Bileta"

        serial_no = fields.Char(string="Nr. Serial")
        shfaqje_id = fields.Many2one('shfaqje.filmi', string="Shfaqje")
        rezervim_id = fields.One2many('rezervim.filmi','bileta_id',string="Rezervimi")
        state = fields.Selection(
            [('free', 'Free'), ('rezervuar', 'Rezervuar'), ('konfirmuar', 'Konfirmuar'), ('anulluar', 'Anulluar'),
             ('perfunduar', 'Perfunduar')], default='free', string="State")

        def show_rezervim(self,Context=None):
            return {
                'name': ('Rezervo'),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'rezervim.filmi',
                'view_id': False,
                'type': 'ir.actions.act_window',
                'target': 'new',
                'context': None,
            }



class Rezervim(models.Model):
        _name = "rezervim.filmi"
        _description = "Rezervimi Biletes"

        emer_rezervimi = fields.Char(string="Nr.Rezervimi", readonly=True)
        shfaqje_id = fields.Many2one('shfaqje.filmi', string="Shfaqje")
        orar_fillimi = fields.Datetime(related='shfaqje_id.ora_fillimit', string="Orari Shfaqjes", readonly=True)
        orar_perfundimit = fields.Datetime(related='shfaqje_id.ora_perfundimit', string="Orari i perfundimit Shfaqjes",readonly=True)
        bileta_id = fields.Many2one('bileta.bileta', string="Bileta")
        bileta_nr = fields.Char(related="bileta_id.serial_no", string="Nr Serial", readonly=True)
        payed = fields.Boolean(string="Payed")
        afati_anullimit = fields.Integer(string='Afati i anullimit')
        state = fields.Selection([('regjistruar', 'Regjistruar'), ('rezervuar', 'Rezervo'), ('konfirmuar', 'Konfirmo'), ('anulluar', 'Anullo')],default='regjistruar', string="State")


        @api.model
        def create(self, vals):
            seq = self.env['ir.sequence'].next_by_code('rezervim.filmi') or '/'
            vals['emer_rezervimi'] = seq
            return super(Rezervim, self).create(vals)



        # @api.onchange
        # def ndrysho_(self,val):
        #     for bileta in self:
        #         if bileta.shfaqje_id:
        #             if bileta.shfaqje_id.bileta_id:
        #                 nr = self.env['bileta.bileta'].search(('serial_no','=',bileta.shfaqje_id.bileta_id))
        #                 if nr:
        #                     self.bileta_nr = nr
        #                       val['bileta_nr']= nr
        #                     return super(Rezervim, self).write(val)



        @api.one
        def regjistruar(self):
            self.state = 'regjistruar'

        @api.one
        def rezervuar(self):
            self.state = 'rezervuar'
            for bileta in self:
                if bileta.bileta_id:
                    self.bileta_id.write({'state': 'rezervuar'})

        @api.one
        def konfirmuar(self):
            if self.payed == True:
                self.state = 'konfirmuar'
                self.env['bileta.bileta'].write({'state': 'konfirmuar'})
            else:
                raise UserWarning('JU nuk mund ta konfirmoni rezervimin nqs nuk keni paguar')


        @api.one
        def anulluar(self):
            if self.state == 'konfirmuar':
                current_date = datetime.date.today()
                if self.orar_fillimi:
                    if self.orar_fillimi - current_date < '3':
                        raise UserWarning('Ju nuk mund te anulloni rezervimin tuaj')
                    else:
                        self.state = 'anulluar'
                        self.bileta_id.write({'state':'anulluar'})
