"""
    Fichier : gestion_Motos_marques_crud.py
    Auteur : OM 2021.05.01
    Gestions des "routes" FLASK et des données pour l'association entre les Motos et les marques.
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_MOTO_164.database.database_tools import DBconnection
from APP_MOTO_164.erreurs.exceptions import *

"""
    Nom : motos_marques_afficher
    Auteur : OM 2021.05.01
    Définition d'une "route" /motos_marques_afficher
    
    But : Afficher les Motos avec les marques associés pour chaque Moto.
    
    Paramètres : id_marque_sel = 0 >> tous les Motos.
                 id_marque_sel = "n" affiche le Moto dont l'id est "n"
                 
"""


@app.route("/motos_marques_afficher/<int:id_moto_sel>", methods=['GET', 'POST'])
def motos_marques_afficher(id_moto_sel):
    print(" motos_marques_afficher id_moto_sel ", id_moto_sel)
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                strsql_marques_Motos_afficher_data = """SELECT t_moto.id_moto, modèle_moto, année_moto, nombre_km_moto,couleur_moto, prix_moto, GROUP_CONCAT(marque_moto) AS 'MarqueMoto', GROUP_CONCAT(type_moto) AS 'TypeMoto'
                                                        FROM t_moto
                                                        LEFT JOIN t_marque_moto ON t_moto.id_moto = t_marque_moto.fk_moto
                                                        LEFT JOIN t_marque ON t_marque.id_marque = t_marque_moto.fk_marque
                                                        GROUP BY t_moto.id_moto"""
                if id_moto_sel == 0:
                    # le paramètre 0 permet d'afficher tous les Motos
                    # Sinon le paramètre représente la valeur de l'id du Moto
                    mc_afficher.execute(strsql_marques_Motos_afficher_data)
                else:
                    # Constitution d'un dictionnaire pour associer l'id du Moto sélectionné avec un nom de variable
                    valeur_id_moto_selected_dictionnaire = {"value_id_moto_selected": id_moto_sel}
                    # En MySql l'instruction HAVING fonctionne comme un WHERE... mais doit être associée à un GROUP BY
                    # L'opérateur += permet de concaténer une nouvelle valeur à la valeur de gauche préalablement définie.
                    strsql_marques_Motos_afficher_data += """ HAVING id_moto = %(value_id_moto_selected)s"""

                    mc_afficher.execute(strsql_marques_Motos_afficher_data, valeur_id_moto_selected_dictionnaire)

                # Récupère les données de la requête.
                data_marques_Motos_afficher = mc_afficher.fetchall()
                print("data_marques ", data_marques_Motos_afficher, " Type : ", type(data_marques_Motos_afficher))

                # Différencier les messages.
                if not data_marques_Motos_afficher and id_moto_sel == 0:
                    flash("""La table "t_moto" est vide. !""", "warning")
                elif not data_marques_Motos_afficher and id_moto_sel > 0:
                    # Si l'utilisateur change l'id_Moto dans l'URL et qu'il ne correspond à aucun Moto
                    flash(f"La moto {id_moto_sel} demandé n'existe pas !!", "warning")
                else:
                    flash(f"Données motos et personne affichés !!", "success")

        except Exception as Exception_motos_marques_afficher:
            raise ExceptionMotosmarquesAfficher(f"fichier : {Path(__file__).name}  ;  {motos_marques_afficher.__name__} ;"
                                               f"{Exception_motos_marques_afficher}")

    print("motos_marques_afficher  ", data_marques_Motos_afficher)
    # Envoie la page "HTML" au serveur.
    return render_template("motos_marques/motos_marques_afficher.html", data=data_marques_Motos_afficher)


"""
    nom: edit_marque_moto_selected
    On obtient un objet "objet_dumpbd"

    Récupère la liste de tous les marques du Moto sélectionné par le bouton "MODIFIER" de "motos_marques_afficher.html"
    
    Dans une liste déroulante particulière (tags-selector-tagselect), on voit :
    1) Tous les marques contenus dans la "t_marque".
    2) Les marques attribués au Moto selectionné.
    3) Les marques non-attribués au Moto sélectionné.

    On signale les erreurs importantes

"""


@app.route("/edit_marque_moto_selected", methods=['GET', 'POST'])
def edit_marque_moto_selected():
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                strsql_marques_afficher = """SELECT id_marque, marque_moto FROM t_marque ORDER BY id_marque ASC"""
                mc_afficher.execute(strsql_marques_afficher)
            data_marques_all = mc_afficher.fetchall()
            print("dans edit_marque_moto_selected ---> data_marques_all", data_marques_all)

            # Récupère la valeur de "id_Moto" du formulaire html "motos_marques_afficher.html"
            # l'utilisateur clique sur le bouton "Modifier" et on récupère la valeur de "id_Moto"
            # grâce à la variable "id_Moto_marques_edit_html" dans le fichier "motos_marques_afficher.html"
            # href="{{ url_for('edit_marque_moto_selected', id_Moto_marques_edit_html=row.id_Moto) }}"
            id_Moto_marques_edit = request.values['id_Moto_marques_edit_html']

            # Mémorise l'id du Moto dans une variable de session
            # (ici la sécurité de l'application n'est pas engagée)
            # il faut éviter de stocker des données sensibles dans des variables de sessions.
            session['session_id_Moto_marques_edit'] = id_Moto_marques_edit

            # Constitution d'un dictionnaire pour associer l'id du Moto sélectionné avec un nom de variable
            valeur_id_moto_selected_dictionnaire = {"value_id_moto_selected": id_Moto_marques_edit}

            # Récupère les données grâce à 3 requêtes MySql définie dans la fonction marques_Motos_afficher_data
            # 1) Sélection du Moto choisi
            # 2) Sélection des marques "déjà" attribués pour le Moto.
            # 3) Sélection des marques "pas encore" attribués pour le Moto choisi.
            # ATTENTION à l'ordre d'assignation des variables retournées par la fonction "marques_Motos_afficher_data"
            data_marque_Moto_selected, data_marques_Motos_non_attribues, data_marques_Motos_attribues = \
                marques_Motos_afficher_data(valeur_id_moto_selected_dictionnaire)

            print(data_marque_Moto_selected)
            lst_data_Moto_selected = [item['id_moto'] for item in data_marque_Moto_selected]
            print("lst_data_Moto_selected  ", lst_data_Moto_selected,
                  type(lst_data_Moto_selected))

            # Dans le composant "tags-selector-tagselect" on doit connaître
            # les marques qui ne sont pas encore sélectionnés.
            lst_data_marques_Motos_non_attribues = [item['id_marque'] for item in data_marques_Motos_non_attribues]
            session['session_lst_data_marques_Motos_non_attribues'] = lst_data_marques_Motos_non_attribues
            print("lst_data_marques_Motos_non_attribues  ", lst_data_marques_Motos_non_attribues,
                  type(lst_data_marques_Motos_non_attribues))

            # Dans le composant "tags-selector-tagselect" on doit connaître
            # les marques qui sont déjà sélectionnés.
            lst_data_marques_Motos_old_attribues = [item['id_marque'] for item in data_marques_Motos_attribues]
            session['session_lst_data_marques_Motos_old_attribues'] = lst_data_marques_Motos_old_attribues
            print("lst_data_marques_Motos_old_attribues  ", lst_data_marques_Motos_old_attribues,
                  type(lst_data_marques_Motos_old_attribues))

            print(" data data_marque_Moto_selected", data_marque_Moto_selected, "type ", type(data_marque_Moto_selected))
            print(" data data_marques_Motos_non_attribues ", data_marques_Motos_non_attribues, "type ",
                  type(data_marques_Motos_non_attribues))
            print(" data_marques_Motos_attribues ", data_marques_Motos_attribues, "type ",
                  type(data_marques_Motos_attribues))

            # Extrait les valeurs contenues dans la table "t_marques", colonne "intitule_marque"
            # Le composant javascript "tagify" pour afficher les tags n'a pas besoin de l'id_marque
            lst_data_marques_Motos_non_attribues = [item['marque_moto'] for item in data_marques_Motos_non_attribues]
            print("lst_all_marques gf_edit_marque_moto_selected ", lst_data_marques_Motos_non_attribues,
                  type(lst_data_marques_Motos_non_attribues))

        except Exception as Exception_edit_marque_moto_selected:
            raise ExceptionEditmarqueMotoselected(f"fichier : {Path(__file__).name}  ;  "
                                                 f"{edit_marque_moto_selected.__name__} ; "
                                                 f"{Exception_edit_marque_moto_selected}")

    return render_template("Motos_marques/Motos_marques_modifier_tags_dropbox.html",
                           data_marques=data_marques_all,
                           data_Moto_selected=data_marque_Moto_selected,
                           data_marques_attribues=data_marques_Motos_attribues,
                           data_marques_non_attribues=data_marques_Motos_non_attribues)


"""
    nom: update_marque_Moto_selected

    Récupère la liste de tous les marques du Moto sélectionné par le bouton "MODIFIER" de "motos_marques_afficher.html"
    
    Dans une liste déroulante particulière (tags-selector-tagselect), on voit :
    1) Tous les marques contenus dans la "t_marque".
    2) Les marques attribués au Moto selectionné.
    3) Les marques non-attribués au Moto sélectionné.

    On signale les erreurs importantes
"""


@app.route("/update_marque_Moto_selected", methods=['GET', 'POST'])
def update_marque_Moto_selected():
    if request.method == "POST":
        try:
            # Récupère l'id du Moto sélectionné
            id_moto_selected = session['session_id_Moto_marques_edit']
            print("session['session_id_Moto_marques_edit'] ", session['session_id_Moto_marques_edit'])

            # Récupère la liste des marques qui ne sont pas associés au Moto sélectionné.
            old_lst_data_marques_Motos_non_attribues = session['session_lst_data_marques_Motos_non_attribues']
            print("old_lst_data_marques_Motos_non_attribues ", old_lst_data_marques_Motos_non_attribues)

            # Récupère la liste des marques qui sont associés au Moto sélectionné.
            old_lst_data_marques_Motos_attribues = session['session_lst_data_marques_Motos_old_attribues']
            print("old_lst_data_marques_Motos_old_attribues ", old_lst_data_marques_Motos_attribues)

            # Effacer toutes les variables de session.
            session.clear()

            # Récupère ce que l'utilisateur veut modifier comme marques dans le composant "tags-selector-tagselect"
            # dans le fichier "marques_Motos_modifier_tags_dropbox.html"
            new_lst_str_marques_Motos = request.form.getlist('name_select_tags')
            print("new_lst_str_marques_Motos ", new_lst_str_marques_Motos)

            # OM 2021.05.02 Exemple : Dans "name_select_tags" il y a ['4','65','2']
            # On transforme en une liste de valeurs numériques. [4,65,2]
            new_lst_int_marque_moto_old = list(map(int, new_lst_str_marques_Motos))
            print("new_lst_marque_moto ", new_lst_int_marque_moto_old, "type new_lst_marque_moto ",
                  type(new_lst_int_marque_moto_old))

            # Pour apprécier la facilité de la vie en Python... "les ensembles en Python"
            # https://fr.wikibooks.org/wiki/Programmation_Python/Ensembles
            # OM 2021.05.02 Une liste de "id_marque" qui doivent être effacés de la table intermédiaire "t_marque_moto".
            lst_diff_marques_delete_b = list(set(old_lst_data_marques_Motos_attribues) -
                                            set(new_lst_int_marque_moto_old))
            print("lst_diff_marques_delete_b ", lst_diff_marques_delete_b)

            # Une liste de "id_marque" qui doivent être ajoutés à la "t_marque_moto"
            lst_diff_marques_insert_a = list(
                set(new_lst_int_marque_moto_old) - set(old_lst_data_marques_Motos_attribues))
            print("lst_diff_marques_insert_a ", lst_diff_marques_insert_a)

            # SQL pour insérer une nouvelle association entre
            # "fk_moto"/"id_Moto" et "fk_marque"/"id_marque" dans la "t_marque_moto"
            strsql_insert_marque_moto = """INSERT INTO t_marque_moto (id_marque_moto, fk_marque, fk_moto)
                                                    VALUES (NULL, %(value_fk_marque)s, %(value_fk_moto)s)"""

            # SQL pour effacer une (des) association(s) existantes entre "id_Moto" et "id_marque" dans la "t_marque_moto"
            strsql_delete_marque_Moto = """DELETE FROM t_marque_moto WHERE fk_marque = %(value_fk_marque)s AND fk_moto = %(value_fk_moto)s"""

            with DBconnection() as mconn_bd:
                # Pour le Moto sélectionné, parcourir la liste des marques à INSÉRER dans la "t_marque_moto".
                # Si la liste est vide, la boucle n'est pas parcourue.
                for id_marque_ins in lst_diff_marques_insert_a:
                    # Constitution d'un dictionnaire pour associer l'id du Moto sélectionné avec un nom de variable
                    # et "id_marque_ins" (l'id du marque dans la liste) associé à une variable.
                    valeurs_Moto_sel_marque_sel_dictionnaire = {"value_fk_moto": id_moto_selected,
                                                               "value_fk_marque": id_marque_ins}

                    mconn_bd.execute(strsql_insert_marque_moto, valeurs_Moto_sel_marque_sel_dictionnaire)

                # Pour le Moto sélectionné, parcourir la liste des marques à EFFACER dans la "t_marque_moto".
                # Si la liste est vide, la boucle n'est pas parcourue.
                for id_marque_del in lst_diff_marques_delete_b:
                    # Constitution d'un dictionnaire pour associer l'id du Moto sélectionné avec un nom de variable
                    # et "id_marque_del" (l'id du marque dans la liste) associé à une variable.
                    valeurs_Moto_sel_marque_sel_dictionnaire = {"value_fk_moto": id_moto_selected,
                                                               "value_fk_marque": id_marque_del}

                    # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
                    # la subtilité consiste à avoir une méthode "execute" dans la classe "DBconnection"
                    # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "DBconnection"
                    # sera interprété, ainsi on fera automatiquement un commit
                    mconn_bd.execute(strsql_delete_marque_Moto, valeurs_Moto_sel_marque_sel_dictionnaire)

        except Exception as Exception_update_marque_Moto_selected:
            raise ExceptionUpdatemarqueMotoselected(f"fichier : {Path(__file__).name}  ;  "
                                                   f"{update_marque_Moto_selected.__name__} ; "
                                                   f"{Exception_update_marque_Moto_selected}")

    # Après cette mise à jour de la table intermédiaire "t_marque_moto",
    # on affiche les Motos et le(urs) marque(s) associé(s).
    return redirect(url_for('motos_marques_afficher', id_moto_sel=id_moto_selected))


"""
    nom: marques_Motos_afficher_data

    Récupère la liste de tous les marques du Moto sélectionné par le bouton "MODIFIER" de "motos_marques_afficher.html"
    Nécessaire pour afficher tous les "TAGS" des marques, ainsi l'utilisateur voit les marques à disposition

    On signale les erreurs importantes
"""


def marques_Motos_afficher_data(valeur_id_moto_selected_dict):
    print("valeur_id_moto_selected_dict...", valeur_id_moto_selected_dict)
    try:

        strsql_Moto_selected = """SELECT id_moto, marque_moto, modèle_moto, année_moto, prix_moto, nombre_km_moto, GROUP_CONCAT(id_marque) as 'MarqueMoto' FROM t_marque_moto
                                        INNER JOIN t_moto ON t_moto.id_moto = t_marque_moto.fk_moto
                                        INNER JOIN t_marque ON t_marque.id_marque = t_marque_moto.fk_marque
                                        WHERE id_moto = %(value_id_moto_selected)s"""

        strsql_marques_Motos_non_attribues = """SELECT id_marque, marque_moto FROM t_marque WHERE id_marque not in(SELECT id_marque as idMarqueMoto FROM t_marque_moto
                                                    INNER JOIN t_moto ON t_moto.id_moto = t_marque_moto.fk_moto
                                                    INNER JOIN t_marque ON t_marque.id_marque = t_marque_moto.fk_marque
                                                    WHERE id_moto = %(value_id_moto_selected)s)"""

        strsql_marques_Motos_attribues = """SELECT id_moto, id_marque, marque_moto FROM t_marque_moto
                                            INNER JOIN t_moto ON t_moto.id_moto = t_marque_moto.fk_moto
                                            INNER JOIN t_marque ON t_marque.id_marque = t_marque_moto.fk_marque
                                            WHERE id_moto = %(value_id_moto_selected)s"""

        # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
        with DBconnection() as mc_afficher:
            # Envoi de la commande MySql
            mc_afficher.execute(strsql_marques_Motos_non_attribues, valeur_id_moto_selected_dict)
            # Récupère les données de la requête.
            data_marques_Motos_non_attribues = mc_afficher.fetchall()
            # Affichage dans la console
            print("marques_Motos_afficher_data ----> data_marques_Motos_non_attribues ", data_marques_Motos_non_attribues,
                  " Type : ",
                  type(data_marques_Motos_non_attribues))

            # Envoi de la commande MySql
            mc_afficher.execute(strsql_Moto_selected, valeur_id_moto_selected_dict)
            # Récupère les données de la requête.
            data_Moto_selected = mc_afficher.fetchall()
            # Affichage dans la console
            print("data_Moto_selected  ", data_Moto_selected, " Type : ", type(data_Moto_selected))

            # Envoi de la commande MySql
            mc_afficher.execute(strsql_marques_Motos_attribues, valeur_id_moto_selected_dict)
            # Récupère les données de la requête.
            data_marques_Motos_attribues = mc_afficher.fetchall()
            # Affichage dans la console
            print("data_marques_Motos_attribues ", data_marques_Motos_attribues, " Type : ",
                  type(data_marques_Motos_attribues))

            # Retourne les données des "SELECT"
            return data_Moto_selected, data_marques_Motos_non_attribues, data_marques_Motos_attribues

    except Exception as Exception_marques_Motos_afficher_data:
        raise ExceptionmarquesMotosAfficherData(f"fichier : {Path(__file__).name}  ;  "
                                               f"{marques_Motos_afficher_data.__name__} ; "
                                               f"{Exception_marques_Motos_afficher_data}")
