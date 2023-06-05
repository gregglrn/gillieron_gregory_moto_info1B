"""Gestion des formulaires avec WTF pour les Motos
Fichier : gestion_Motos_wtf_forms.py
Auteur : OM 2022.04.11

"""
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField
from wtforms import SubmitField
from wtforms.validators import Length, InputRequired, NumberRange, DataRequired
from wtforms.validators import Regexp
from wtforms.widgets import TextArea


class FormWTFAddMoto(FlaskForm):
    """
        Dans le formulaire "marques_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    modèle_moto_regexp = "^[A-Za-z0-9\-]+$"


    
    modèle_moto_add_wtf = StringField("Modèle de la Moto ", validators=[Length(min=2, max=2000, message="min 2 max 20"),
                                                               Regexp(modèle_moto_regexp,
                                                                      message="Pas de caractères "
                                                                              "spéciaux, "
                                                                              "d'espace à double, de double "
                                                                              "apostrophe")
                                                               ])

    submit = SubmitField("Enregistrer la moto")


class FormWTFUpdateMoto(FlaskForm):
    """
        Dans le formulaire "Moto_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    année_moto_regexp = "^(19|20)\d{2}$"

    modèle_moto_update_wtf = StringField("Clavioter le modèle de la moto", validators=[Length(min=2, max=20, message="min 2 max 20")])
    année_moto_update_wtf = StringField("Clavioter l'année de la moto", validators=[Length(min=4, max=4, message="année invalide"),
                                                                                    Regexp(année_moto_regexp,
                                                                                           message="année invalide")
                                                                                    ])

    couleur_moto_update_wtf = StringField("Couleur de la moto", validators=[Length(min=2, max=20, message="min 2 max 20")])
    prix_moto_update_wtf = StringField("Prix de la moto", validators=[Length(min=2, max=20, message="min 2 max 20")])
    nombre_km_moto_update_wtf = StringField("Nombre de km de la moto", validators=[Length(min=2, max=20, message="min 2 max 20")])
    submit = SubmitField("Update moto")


class FormWTFDeleteMoto(FlaskForm):
    """
        Dans le formulaire "moto_delete_wtf.html"

        modèle_moto_delete_wtf : Champ qui reçoit la valeur du Moto, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "Moto".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_Moto".
    """
    modèle_moto_delete_wtf = StringField("Effacer cette moto")
    submit_btn_del_moto = SubmitField("Effacer moto")
    submit_btn_conf_del_moto = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
