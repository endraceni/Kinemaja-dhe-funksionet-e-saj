import base64

from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError, UserError
from odoo.modules.module import get_module_resource


class Filmi(models.Model):
    _name = "film.film"
    _description = "Filmi"

    img = fields.Binary(string="Image", default='_default_image', attachment=True)
    id_kategori = fields.Many2one('kategori.kategori', string="ID_Kategori")
    name = fields.Char(string="Titulli", required=True)
    imdb_rate = fields.Float(string="IMBD", required=True)
    aktore = fields.Text(string="Aktoret", required=True)
    regjizori = fields.Char(string="Regjizor", required=True)
    permbajtja = fields.Text(string="Permbajtja", required=True)
    viti_prodhimit = fields.Date(string="Data Prodhimit")
    gjuha = fields.Selection(
        [('mandarin', 'Mandarin'), ('spanish', 'Spanish'), ('english', 'English'), ('hindi[a]', 'Hindi[a]'),
         ('arabic', 'Arabic'),
         ('portuguese', 'Portuguese'), ('bengali', 'Bengali'), ('russian', 'Russian'), ('japanese', 'Japanese'),
         ('german', 'German'), ('vietnamese', 'Vietnamese'),
         ('korean', 'Korean'), ('french', 'French'), ('urdu', 'Urdu'), ('turkish', 'Turkish'), ('italian', 'Italian'),
         ('albanian', 'Albanian')
            , ('romanian', 'Romanian'), ('serbo-Croatian ', 'Serbo-Croatian '), ('greek', 'Greek'),
         ('swedish', 'Swedish')], string="Gjuha")
    premiere = fields.Boolean('Premiere', default=True)

    @api.model
    def _default_image(self):
        image_path = get_module_resource('kinema', 'static/src/', 'night_school.png')
        return tools.image_resize_image_big(base64.b64encode(open(image_path, 'rb').read()))


class Kategoria(models.Model):
    _name = "kategori.kategori"
    _description = "Kategorite e filmave"

    name = fields.Selection([('Aksion', 'aksion'), ('Animuar', 'animuar'), ('Aventure', 'aventure'), ('Aziatik', 'aziatik'),('Biografi', 'biografi'), ('Dokumentar', 'dokumentar'), ('Drama', 'drama'),
                             ('Fantashkence', 'fantashkence'),('Filozofik', 'filozofik'), ('Historik', 'historik'),('Horror', 'horror'), ('Komedi', 'komedi'), ('Krim', 'krim'), ('Mister', 'mister'),
                             ('Musical', 'musical'),('Politik', 'politik'), ('Romance', 'romance'), ('Thriller', 'thriller')], string="Kategorite")

    film_id = fields.One2many('film.film', 'id_kategori', string="Film")