"""
    Fichier : gestion_marques_wtf_forms.py
    Auteur : OM 2021.03.22
    Gestion des formulaires avec WTF
"""
from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms import SubmitField
from wtforms.validators import Length, InputRequired, DataRequired
from wtforms.validators import Regexp


class FormWTFAjoutermarques(FlaskForm):
    """
        Dans le formulaire "marques_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_marque_regexp = "^[A-Za-z0-9\-]+$"

    nom_marque_wtf = StringField("Clavioter le nom de la marque de la moto ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                   Regexp(nom_marque_regexp,
                                                                          message="Pas de chiffres, de caractères "
                                                                                  "spéciaux, "
                                                                                  "d'espace à double, de double "
                                                                                  "apostrophe, de double trait union")
                                                                   ])
    submit = SubmitField("Enregistrer la marque")


class FormWTFUpdatemarque(FlaskForm):
    """
        Dans le formulaire "marque_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_marque_update_regexp = "^[A-Za-z0-9\-]+$"
    nom_marque_update_wtf = StringField("Nom de la marque de la moto ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                          Regexp(nom_marque_update_regexp,
                                                                                 message="Pas de chiffres, de "
                                                                                         "caractères "
                                                                                         "spéciaux, "
                                                                                         "d'espace à double, de double "
                                                                                         "apostrophe, de double trait "
                                                                                         "union")
                                                                          ])
    date_marque_wtf_essai = StringField("Type de moto", validators=[InputRequired("type obligatoire"),
                                                               DataRequired("type non valide")])
    submit = SubmitField("Update marque")


class FormWTFDeletemarque(FlaskForm):
    """
        Dans le formulaire "marques_delete_wtf.html"

        nom_marque_delete_wtf : Champ qui reçoit la valeur du marque, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "marque".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_marque".
    """
    nom_marque_delete_wtf = StringField("Effacer cette marque")
    submit_btn_del = SubmitField("Effacer marque")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
