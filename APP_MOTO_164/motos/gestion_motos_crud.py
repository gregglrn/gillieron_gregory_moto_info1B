"""Gestion des "routes" FLASK et des données pour les Motos.
Fichier : gestion_Motos_crud.py
Auteur : OM 2022.04.11
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_MOTO_164.database.database_tools import DBconnection
from APP_MOTO_164.erreurs.exceptions import *
from APP_MOTO_164.motos.gestion_motos_wtf_forms import FormWTFUpdateMoto, FormWTFAddMoto, FormWTFDeleteMoto

"""Ajouter un Moto grâce au formulaire "Moto_add_wtf.html"
Auteur : OM 2022.04.11
Définition d'une "route" /Moto_add

Test : exemple: cliquer sur le menu "Motos/marques" puis cliquer sur le bouton "ADD" d'un "Moto"

Paramètres : sans


Remarque :  Dans le champ "modèle_moto_update_wtf" du formulaire "Motos/Motos_update_wtf.html",
            le contrôle de la saisie s'effectue ici en Python dans le fichier ""
            On ne doit pas accepter un champ vide.
"""


@app.route("/Moto_add", methods=['GET', 'POST'])
def Moto_add_wtf():
    # Objet formulaire pour AJOUTER un Moto
    form_add_Moto = FormWTFAddMoto()
    if request.method == "POST":
        try:
            if form_add_Moto.validate_on_submit():
                nom_Moto_add = form_add_Moto.modèle_moto_add_wtf.data

                valeurs_insertion_dictionnaire = {"value_modèle_moto": nom_Moto_add}
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_Moto = """INSERT INTO t_moto (id_moto,modèle_moto) VALUES (NULL,%(value_modèle_moto)s) """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_Moto, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion du nouveau Moto (id_moto_sel=0 => afficher tous les Motos)
                return redirect(url_for('motos_marques_afficher', id_moto_sel=0))

        except Exception as Exception_marques_ajouter_wtf:
            raise ExceptionmarquesAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{Moto_add_wtf.__name__} ; "
                                            f"{Exception_marques_ajouter_wtf}")

    return render_template("Motos/Moto_add_wtf.html", form_add_Moto=form_add_Moto)


"""Editer(update) un Moto qui a été sélectionné dans le formulaire "motos_marques_afficher.html"
Auteur : OM 2022.04.11
Définition d'une "route" /Moto_update

Test : exemple: cliquer sur le menu "Motos/marques" puis cliquer sur le bouton "EDIT" d'un "Moto"

Paramètres : sans

But : Editer(update) un marque qui a été sélectionné dans le formulaire "marques_afficher.html"

Remarque :  Dans le champ "modèle_moto_update_wtf" du formulaire "Motos/Motos_update_wtf.html",
            le contrôle de la saisie s'effectue ici en Python.
            On ne doit pas accepter un champ vide.
"""


@app.route("/Moto_update", methods=['GET', 'POST'])
def Moto_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_Moto"
    id_Moto_update = request.values['id_Moto_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update_moto = FormWTFUpdateMoto()
    try:
        print(" on submit ", form_update_moto.validate_on_submit())
        if form_update_moto.validate_on_submit():
            # Récupèrer la valeur du champ depuis "marque_update_wtf.html" après avoir cliqué sur "SUBMIT".
            modèle_moto_update = form_update_moto.modèle_moto_update_wtf.data
            année_moto_update = form_update_moto.année_moto_update_wtf.data
            couleur_moto_update = form_update_moto.couleur_moto_update_wtf.data
            prix_moto_update = form_update_moto.prix_moto_update_wtf.data
            nombre_km_moto_update = form_update_moto.nombre_km_moto_update_wtf.data

            valeur_update_dictionnaire = {"value_id_moto": id_Moto_update,
                                          "value_modèle_moto": modèle_moto_update,
                                          "value_nombre_km_moto": nombre_km_moto_update,
                                          "value_année_moto": année_moto_update,
                                          "value_prix_moto": prix_moto_update,
                                          "value_couleur_moto": couleur_moto_update
                                          }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_nom_Moto = """UPDATE t_moto SET modèle_moto = %(value_modèle_moto)s,
                                                            nombre_km_moto = %(value_nombre_km_moto)s,
                                                            année_moto = %(value_année_moto)s,
                                                            prix_moto = %(value_prix_moto)s,
                                                            couleur_moto = %(value_couleur_moto)s
                                                            WHERE id_moto = %(value_id_moto)s"""
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_nom_Moto, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Afficher seulement le Moto modifié, "ASC" et l'"id_Moto_update"
            return redirect(url_for('motos_marques_afficher', id_moto_sel=id_Moto_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_Moto" et "intitule_marque" de la "t_marque"
            str_sql_id_Moto = "SELECT * FROM t_moto WHERE id_moto = %(value_id_moto)s"
            valeur_select_dictionnaire = {"value_id_moto": id_Moto_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_Moto, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom marque" pour l'UPDATE
            data_Moto = mybd_conn.fetchone()
            print("data_Moto ", data_Moto, " type ", type(data_Moto), " marque ",
                  data_Moto["modèle_moto"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "Moto_update_wtf.html"
            form_update_moto.modèle_moto_update_wtf.data = data_Moto["modèle_moto"]
            form_update_moto.année_moto_update_wtf.data = data_Moto["année_moto"]
            # Debug simple pour contrôler la valeur dans la console "run" de PyCharm
            print(f" année_moto  ", data_Moto["modèle_moto"], "  type ", type(data_Moto["modèle_moto"]))
            form_update_moto.couleur_moto_update_wtf.data = data_Moto["couleur_moto"]
            form_update_moto.prix_moto_update_wtf.data = data_Moto["prix_moto"]
            form_update_moto.nombre_km_moto_update_wtf.data = data_Moto["nombre_km_moto"]

    except Exception as Exception_Moto_update_wtf:
        raise ExceptionMotoUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                     f"{Moto_update_wtf.__name__} ; "
                                     f"{Exception_Moto_update_wtf}")

    return render_template("Motos/Moto_update_wtf.html", form_update_moto=form_update_moto)


"""Effacer(delete) un Moto qui a été sélectionné dans le formulaire "motos_marques_afficher.html"
Auteur : OM 2022.04.11
Définition d'une "route" /moto_delete
    
Test : ex. cliquer sur le menu "Moto" puis cliquer sur le bouton "DELETE" d'un "Moto"
    
Paramètres : sans

Remarque :  Dans le champ "modèle_moto_delete_wtf" du formulaire "Motos/moto_delete_wtf.html"
            On doit simplement cliquer sur "DELETE"
"""


@app.route("/moto_delete", methods=['GET', 'POST'])
def moto_delete_wtf():
    # Pour afficher ou cacher les boutons "EFFACER"
    data_moto_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_moto"
    id_moto_delete = request.values['id_moto_btn_delete_html']

    # Objet formulaire pour effacer la moto sélectionné.
    form_delete_moto = FormWTFDeleteMoto()
    try:
        # Si on clique sur "ANNULER", afficher toutes les motos.
        if form_delete_moto.submit_btn_annuler.data:
            return redirect(url_for("motos_marques_afficher", id_moto_sel=0))

        if form_delete_moto.submit_btn_conf_del_moto.data:
            # Récupère les données afin d'afficher à nouveau
            # le formulaire "motos/moto_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
            data_moto_delete = session['data_moto_delete']
            print("data_moto_delete ", data_moto_delete)

            flash(f"Effacer la moto de façon définitive de la BD !!!", "danger")
            # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
            # On affiche le bouton "Effacer marque" qui va irrémédiablement EFFACER le marque
            btn_submit_del = True

        # L'utilisateur a vraiment décidé d'effacer.
        if form_delete_moto.submit_btn_del_moto.data:
            valeur_delete_dictionnaire = {"value_id_moto": id_moto_delete}
            print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

            str_sql_delete_fk_moto_marque = """DELETE FROM t_marque_moto WHERE fk_moto = %(value_id_moto)s"""
            str_sql_delete_moto = """DELETE FROM t_moto WHERE id_moto = %(value_id_moto)s"""
            # Manière brutale d'effacer d'abord la "fk_moto", même si elle n'existe pas dans la "t_marque_moto"
            # Ensuite on peut effacer le Moto vu qu'il n'est plus "lié" (INNODB) dans la "t_marque_moto"
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_delete_fk_moto_marque, valeur_delete_dictionnaire)
                mconn_bd.execute(str_sql_delete_moto, valeur_delete_dictionnaire)

            flash(f"Moto définitivement effacé !!", "success")
            print(f"Moto définitivement effacé !!")

            # afficher les données
            return redirect(url_for('motos_marques_afficher', id_moto_sel=0))
        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_moto": id_moto_delete}
            print(id_moto_delete, type(id_moto_delete))

            # Requête qui affiche le Moto qui doit être efffacé.
            str_sql_marques_Motos_delete = """SELECT * FROM t_moto WHERE id_moto = %(value_id_moto)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_marques_Motos_delete, valeur_select_dictionnaire)
                data_moto_delete = mydb_conn.fetchall()
                print("data_moto_delete...", data_moto_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "Motos/moto_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_moto_delete'] = data_moto_delete

            # Le bouton pour l'action "DELETE" dans le form. "moto_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_moto_delete_wtf:
        raise ExceptionMotoDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                     f"{moto_delete_wtf.__name__} ; "
                                     f"{Exception_moto_delete_wtf}")

    return render_template("Motos/moto_delete_wtf.html",
                           form_delete_moto=form_delete_moto,
                           btn_submit_del=btn_submit_del,
                           data_Moto_del=data_moto_delete
                           )
