"""
    Fichier : gestion_marques_wtf_forms.py
    Auteur : OM 2021.03.22
    Gestion des formulaires avec WTF

    But : Essayer un formulaire avec WTForms
"""

from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms import PasswordField
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.validators import Regexp


class MonPremierWTForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(message="Mot de passe indispensable !")])

    nom_marque_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_marque_wtf = StringField("Clavioter le marque ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                   Regexp(nom_marque_regexp,
                                                                          message="Pas de chiffres, de caractères "
                                                                                  "spéciaux, d'espace à double, "
                                                                                  "de double apostrophe, "
                                                                                  "de double trait union")
                                                                   ])

    case_cocher_npc = BooleanField('Ne pas cliquer')

    submit = SubmitField('Ok !')
