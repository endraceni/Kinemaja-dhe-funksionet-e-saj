import base64

from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError, UserError
from odoo.modules.module import get_module_resource


class Filmi(models.Model):
    _name = "film.film"
    _description = "Filmi"

    img = fields.Binary(string="Image", default='_default_image', attachment=True)
    name = fields.Char(string="Titulli", required=True)
    kategori = fields.Selection(
        [('Aksion', 'aksion'), ('Animuar', 'animuar'), ('Aventure', 'aventure'), ('Aziatik', 'aziatik'),
         ('Biografi', 'biografi'), ('Dokumentar', 'dokumentar'), ('Drama', 'drama'),
         ('Fantashkence', 'fantashkence'), ('Filozofik', 'filozofik'), ('Historik', 'historik'), ('Horror', 'horror'),
         ('Komedi', 'komedi'), ('Krim', 'krim'), ('Mister', 'mister'),
         ('Musical', 'musical'), ('Politik', 'politik'), ('Romance', 'romance'), ('Thriller', 'thriller')],
        string="Kategorite")
    imdb_rate = fields.Float(string="IMBD", required=True)
    aktore = fields.Text(string="Aktoret", required=True)
    regjizori = fields.Char(string="Regjizor", required=True)
    permbajtja = fields.Text(string="Permbajtja", required=True)
    viti_prodhimit = fields.Date(string="Data Prodhimit")
    gjuha = fields.Selection([('mandarin', 'Mandarin'), ('spanish', 'Spanish'), ('english', 'English'), ('hindi[a]', 'Hindi[a]'),
         ('arabic', 'Arabic'),('portuguese', 'Portuguese'), ('bengali', 'Bengali'), ('russian', 'Russian'), ('japanese', 'Japanese'),
         ('german', 'German'), ('vietnamese', 'Vietnamese'),('korean', 'Korean'), ('french', 'French'), ('urdu', 'Urdu'), ('turkish', 'Turkish'), ('italian', 'Italian'),
         ('albanian', 'Albanian'), ('romanian', 'Romanian'), ('serbo-Croatian ', 'Serbo-Croatian '), ('greek', 'Greek'),('swedish', 'Swedish')], string="Gjuha")
    premiere = fields.Boolean('Premiere', default=True)


