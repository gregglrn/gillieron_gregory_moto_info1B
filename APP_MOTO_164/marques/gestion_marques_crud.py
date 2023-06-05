"""Gestion des "routes" FLASK et des données pour les marques.
Fichier : gestion_marques_crud.py
Auteur : OM 2021.03.16
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_MOTO_164 import app
from APP_MOTO_164.database.database_tools import DBconnection
from APP_MOTO_164.erreurs.exceptions import *
from APP_MOTO_164.marques.gestion_marques_wtf_forms import FormWTFAjoutermarques
from APP_MOTO_164.marques.gestion_marques_wtf_forms import FormWTFDeletemarque
from APP_MOTO_164.marques.gestion_marques_wtf_forms import FormWTFUpdatemarque

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /marques_afficher
    
    Test : ex : http://127.0.0.1:5575/marques_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_marque_sel = 0 >> tous les marques.
                id_marque_sel = "n" affiche le marque dont l'id est "n"
"""


@app.route("/marques_afficher/<string:order_by>/<int:id_marque_sel>", methods=['GET', 'POST'])
def marques_afficher(order_by, id_marque_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_marque_sel == 0:
                    strsql_marques_afficher = """SELECT * FROM t_marque"""
                    mc_afficher.execute(strsql_marques_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_marque"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du marque sélectionné avec un nom de variable
                    valeur_id_marque_selected_dictionnaire = {"value_id_marque_selected": id_marque_sel}
                    strsql_marques_afficher = """SELECT * FROM t_marque WHERE id_marque = %(value_id_marque_selected)s"""

                    mc_afficher.execute(strsql_marques_afficher, valeur_id_marque_selected_dictionnaire)
                else:
                    strsql_marques_afficher = """SELECT * FROM t_marque"""

                    mc_afficher.execute(strsql_marques_afficher)

                data_marques = mc_afficher.fetchall()

                print("data_marques ", data_marques, " Type : ", type(data_marques))

                # Différencier les messages si la table est vide.
                if not data_marques and id_marque_sel == 0:
                    flash("""La table "t_marque" est vide. !!""", "warning")
                elif not data_marques and id_marque_sel > 0:
                    # Si l'utilisateur change l'id_marque dans l'URL et que le marque n'existe pas,
                    flash(f"La personne demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_marque" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données marques affichés !!", "success")

        except Exception as Exception_marques_afficher:
            raise ExceptionmarquesAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{marques_afficher.__name__} ; "
                                          f"{Exception_marques_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("marques/marques_afficher.html", data=data_marques)


"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /marques_ajouter
    
    Test : ex : http://127.0.0.1:5575/marques_ajouter
    
    Paramètres : sans
    
    But : Ajouter un marque pour un Moto
    
    Remarque :  Dans le champ "name_marque_html" du formulaire "marques/marques_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/marques_ajouter", methods=['GET', 'POST'])
def marques_ajouter_wtf():
    form = FormWTFAjoutermarques()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                name_marque_wtf = form.nom_marque_wtf.data
                name_marque = name_marque_wtf.lower()
                valeurs_insertion_dictionnaire = {"value_intitule_marque": name_marque}
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_marque = """INSERT INTO t_marque (id_marque, marque_moto) VALUES (NULL,%(value_intitule_marque)s) """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_marque, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('marques_afficher', order_by='DESC', id_marque_sel=0))

        except Exception as Exception_marques_ajouter_wtf:
            raise ExceptionmarquesAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{marques_ajouter_wtf.__name__} ; "
                                            f"{Exception_marques_ajouter_wtf}")

    return render_template("marques/marques_ajouter_wtf.html", form=form)


"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /marque_update
    
    Test : ex cliquer sur le menu "marques" puis cliquer sur le bouton "EDIT" d'un "marque"
    
    Paramètres : sans
    
    But : Editer(update) un marque qui a été sélectionné dans le formulaire "marques_afficher.html"
    
    Remarque :  Dans le champ "nom_marque_update_wtf" du formulaire "marques/marque_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/marque_update", methods=['GET', 'POST'])
def marque_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_marque"
    id_marque_update = request.values['id_marque_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdatemarque()
    try:
        print(" on submit ", form_update.validate_on_submit())
        if form_update.validate_on_submit():
            # Récupèrer la valeur du champ depuis "marque_update_wtf.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            name_marque_update = form_update.nom_marque_update_wtf.data
            name_marque_update = name_marque_update.lower()
            date_marque_essai = form_update.date_marque_wtf_essai.data

            valeur_update_dictionnaire = {"value_id_marque": id_marque_update,
                                          "value_name_marque": name_marque_update,
                                          "value_date_marque_essai": date_marque_essai
                                          }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_intitulemarque = """UPDATE t_marque SET marque_moto = %(value_name_marque)s, 
            type_moto = %(value_date_marque_essai)s WHERE id_marque = %(value_id_marque)s """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_intitulemarque, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_marque_update"
            return redirect(url_for('marques_afficher', order_by="ASC", id_marque_sel=id_marque_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_marque" et "intitule_marque" de la "t_marque"
            str_sql_id_marque = "SELECT id_marque, marque_moto, type_moto FROM t_marque " \
                               "WHERE id_marque = %(value_id_marque)s"
            valeur_select_dictionnaire = {"value_id_marque": id_marque_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_marque, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom marque" pour l'UPDATE
            data_nom_marque = mybd_conn.fetchone()
            print("data_nom_marque ", data_nom_marque, " type ", type(data_nom_marque), " marque ",
                  data_nom_marque["marque_moto"])

            # Afficher la valeur sélectionnée dans les champs du formulaire "marque_update_wtf.html"
            form_update.nom_marque_update_wtf.data = data_nom_marque["marque_moto"]
            form_update.date_marque_wtf_essai.data = data_nom_marque["type_moto"]

    except Exception as Exception_marque_update_wtf:
        raise ExceptionmarqueUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{marque_update_wtf.__name__} ; "
                                      f"{Exception_marque_update_wtf}")

    return render_template("marques/marques_update_wtf.html", form_update=form_update)


"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /marque_delete
    
    Test : ex. cliquer sur le menu "marques" puis cliquer sur le bouton "DELETE" d'un "marque"
    
    Paramètres : sans
    
    But : Effacer(delete) un marque qui a été sélectionné dans le formulaire "marques_afficher.html"
    
    Remarque :  Dans le champ "nom_marque_delete_wtf" du formulaire "marques/marque_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@app.route("/marque_delete", methods=['GET', 'POST'])
def marque_delete_wtf():
    data_Motos_attribue_marque_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_marque"
    id_marque_delete = request.values['id_marque_btn_delete_html']

    # Objet formulaire pour effacer le marque sélectionné.
    form_delete = FormWTFDeletemarque()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("marques_afficher", order_by="ASC", id_marque_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "marques/marque_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_Motos_attribue_marque_delete = session['data_Motos_attribue_marque_delete']
                print("data_Motos_attribue_marque_delete ", data_Motos_attribue_marque_delete)

                flash(f"Effacer la marque de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer marque" qui va irrémédiablement EFFACER le marque
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_marque": id_marque_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_motos_marque = """DELETE FROM t_marque_moto WHERE fk_marque = %(value_id_marque)s"""
                str_sql_delete_idmarque = """DELETE FROM t_marque WHERE id_marque = %(value_id_marque)s"""
                # Manière brutale d'effacer d'abord la "fk_marque", même si elle n'existe pas dans la "t_marque_moto"
                # Ensuite on peut effacer le marque vu qu'il n'est plus "lié" (INNODB) dans la "t_marque_moto"
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_motos_marque, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_idmarque, valeur_delete_dictionnaire)

                flash(f"marque définitivement effacé !!", "success")
                print(f"marque définitivement effacé !!")

                # afficher les données
                return redirect(url_for('marques_afficher', order_by="ASC", id_marque_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_marque": id_marque_delete}
            print(id_marque_delete, type(id_marque_delete))

            # Requête qui affiche tous les Motos_marques qui ont le marque que l'utilisateur veut effacer
            str_sql_marques_Motos_delete = """SELECT id_marque_moto, marque_moto, id_marque, marque_moto FROM t_marque_moto 
                                            INNER JOIN t_moto ON t_marque_moto.fk_moto = t_moto.id_moto
                                            INNER JOIN t_marque ON t_marque_moto.fk_marque = t_marque.id_marque
                                            WHERE fk_marque = %(value_id_marque)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_marques_Motos_delete, valeur_select_dictionnaire)
                data_Motos_attribue_marque_delete = mydb_conn.fetchall()
                print("data_Motos_attribue_marque_delete...", data_Motos_attribue_marque_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "marques/marque_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_Motos_attribue_marque_delete'] = data_Motos_attribue_marque_delete

                # Opération sur la BD pour récupérer "id_marque" et "intitule_marque" de la "t_marque"
                str_sql_id_marque = "SELECT id_marque, marque_moto FROM t_marque WHERE id_marque = %(value_id_marque)s"

                mydb_conn.execute(str_sql_id_marque, valeur_select_dictionnaire)
                # Une seule valeur est suffisante "fetchone()",
                # vu qu'il n'y a qu'un seul champ "nom marque" pour l'action DELETE
                data_nom_marque = mydb_conn.fetchone()
                print("data_nom_marque ", data_nom_marque, " type ", type(data_nom_marque), " marque ",
                      data_nom_marque["marque_moto"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "marque_delete_wtf.html"
            form_delete.nom_marque_delete_wtf.data = data_nom_marque["marque_moto"]

            # Le bouton pour l'action "DELETE" dans le form. "marque_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_marque_delete_wtf:
        raise ExceptionmarqueDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{marque_delete_wtf.__name__} ; "
                                      f"{Exception_marque_delete_wtf}")

    return render_template("marques/marque_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_Motos_associes=data_Motos_attribue_marque_delete)
