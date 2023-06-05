"""
    Fichier : gestion_wtf_forms_demo_select.py
    Auteur : OM 2023.03.26
    Gestions des "routes" FLASK et des données pour des démos sur les listes déroulantes.
"""
import sys

import pymysql
from flask import flash, redirect, url_for
from flask import render_template
from flask import request
from flask import session

from APP_MOTO_164 import app
from APP_MOTO_164.database.database_tools import DBconnection
from APP_MOTO_164.erreurs.msg_erreurs import *
from APP_MOTO_164.essais_wtf_forms.wtf_forms_demo_select import DemoFormSelectWTF

"""
    Auteur : OM 2023.03.26
    Définition d'une "route" /demo_select_wtf
    
    Test : 
    
    Paramètres : sans
    
    But : Montrer qu'il est possible de faire des listes déroulantes-
    
    Remarque :  
"""


@app.route("/demo_select_wtf", methods=['GET', 'POST'])
def demo_select_wtf():
    marque_selectionne = None
    # Objet formulaire pour montrer une liste déroulante basé su    r la table "t_marque"
    form_demo = DemoFormSelectWTF()
    try:
        print("form_demo.submit_btn_ok_dplist_marque.data  ", form_demo.submit_btn_ok_dplist_marque.data)
        if request.method == "POST" and form_demo.submit_btn_ok_dplist_marque.data:

            if form_demo.submit_btn_ok_dplist_marque.data:
                print("marque sélectionné : ",
                      form_demo.marques_dropdown_wtf.data)
                marque_selectionne = form_demo.marques_dropdown_wtf.data
                form_demo.marques_dropdown_wtf.choices = session['marque_val_list_dropdown']
                data_marques = session['data_marques']
                return render_template("zzz_essais_om_104/demo_form_select_wtf.html",
                                       form=form_demo,
                                       marque_selectionne=marque_selectionne,
                                       data_marques_drop_down=data_marques)


        if request.method == "GET":
            with DBconnection() as mc_afficher:
                strsql_marques_afficher = """SELECT id_marque, marque_moto FROM t_marque ORDER BY id_marque ASC"""
                mc_afficher.execute(strsql_marques_afficher)

            data_marques = mc_afficher.fetchall()
            session['data_marques'] = data_marques
            print("demo_select_wtf data_marques ", data_marques, " Type : ", type(data_marques))

            """
                Préparer les valeurs pour la liste déroulante de l'objet "form_demo"
                la liste déroulante est définie dans le "wtf_forms_demo_select.py" 
                le formulaire qui utilise la liste déroulante "zzz_essais_om_104/demo_form_select_wtf.html"
            """
            marque_val_list_dropdown = []
            for i in data_marques:
                marque_val_list_dropdown.append(i['marque_moto'])

            # Aussi possible d'avoir un id numérique et un texte en correspondance
            # marque_val_list_dropdown = [(i["id_marque"], i["intitule_marque"]) for i in data_marques]

            print("marque_val_list_dropdown ", marque_val_list_dropdown)

            form_demo.marques_dropdown_wtf.choices = marque_val_list_dropdown
            session['marque_val_list_dropdown'] = marque_val_list_dropdown
            # Ceci est simplement une petite démo. on fixe la valeur PRESELECTIONNEE de la liste
            form_demo.marques_dropdown_wtf.data = "philosophique"
            marque_selectionne = form_demo.marques_dropdown_wtf.data
            print("marque choisi dans la liste :", marque_selectionne)
            session['marque_selectionne_get'] = marque_selectionne

    # OM 2020.04.16 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
    except KeyError:
        flash(f"__KeyError dans wtf_forms_demo_select : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")
    except ValueError:
        flash(f"Erreur dans wtf_forms_demo_select : {sys.exc_info()[0]} {sys.exc_info()[1]}", "danger")
    except (pymysql.err.OperationalError,
            pymysql.ProgrammingError,
            pymysql.InternalError,
            pymysql.err.IntegrityError,
            TypeError) as erreur_gest_genr_crud:
        code, msg = erreur_gest_genr_crud.args
        flash(f"attention : {error_codes.get(code, msg)} {erreur_gest_genr_crud} ", "danger")

        flash(f"Erreur dans wtf_forms_demo_select : {sys.exc_info()[0]} "
              f"{erreur_gest_genr_crud.args[0]} , "
              f"{erreur_gest_genr_crud}", "danger")

        flash(f"__KeyError dans wtf_forms_demo_select : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")

    return render_template("zzz_essais_om_104/demo_form_select_wtf.html",
                           form=form_demo,
                           marque_selectionne=marque_selectionne,
                           data_marques_drop_down=data_marques)


@app.route("/demo_select_dropdown_bootstrap", methods=['GET', 'POST'])
def demo_select_dropdown_bootstrap():
    print("marque choisi dans la liste :")
    if request.method == 'POST':
        choix_list_drop_down = request.form.getlist("ma_petite_liste_unique")
        print("choix_list_drop_down ", choix_list_drop_down)
        print("choix_list_drop_down form ", request.form["ma_petite_liste_unique"])
        print("choix_list_drop_down form.items() ", request.form.items())

        for key, val in request.form.items():
            print(key, val)

        keys = request.form.keys()
        keys = [key for key in keys]
        print("choix_list_drop_down keys ", keys)

        print("choix_list_drop_down request values ", request.values["ma_petite_liste_unique"])
        print("choix_list_drop_down request data ", request.data)

        for x in choix_list_drop_down:
            print("x", x, "marque ", choix_list_drop_down)

    return render_template("zzz_essais_om_104/essai_form_result_dropdown.html",
                           my_choice_dropdown=x,
                           liste_choice="essai")
