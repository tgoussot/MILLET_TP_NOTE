
from connexion_db import get_db
from flask import *

def find_details_oeuvre_exemplaires(id_oeuvre):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete4_1' FROM DUAL '''
        sql = '''
        SELECT auteur.nom, oeuvre.titre,oeuvre.id_oeuvre, oeuvre.date_parution AS date_parution, COUNT(E1.id_exemplaire) AS nb_exemplaire,
        COUNT(E2.id_exemplaire) AS nb_exemp_dispo
        FROM oeuvre
        INNER JOIN auteur ON oeuvre.auteur_id = auteur.id_auteur
        LEFT JOIN exemplaire AS E1 ON oeuvre.id_oeuvre = E1.oeuvre_id
        LEFT JOIN exemplaire AS E2 ON E2.id_exemplaire = E1.id_exemplaire 
            AND E2.id_exemplaire NOT IN (SELECT emprunt.exemplaire_id FROM emprunt WHERE emprunt.date_retour IS NULL)
        WHERE oeuvre.id_oeuvre = %s
        GROUP BY auteur.nom, oeuvre.titre, oeuvre.date_parution, oeuvre.id_oeuvre
        ORDER BY auteur.nom, oeuvre.titre;'''        
        cursor.execute(sql,(id_oeuvre))
        return cursor.fetchone()
    except ValueError:
        abort(400,'erreur requete 4_1')

def find_exemplaires_oeuvre(id_oeuvre):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete4_2' FROM DUAL '''
        sql = '''
        SELECT
            exemplaire.id_exemplaire AS id_exemplaire,
            exemplaire.etat,
            exemplaire.date_achat,
            exemplaire.prix,
            oeuvre.titre,
            oeuvre.id_oeuvre AS noOeuvre,
            oeuvre.date_parution AS dateParution,
            CASE
                WHEN emprunt.exemplaire_id IS NULL THEN exemplaire.id_exemplaire
                WHEN emprunt.date_retour IS NULL THEN NULL
                ELSE exemplaire.id_exemplaire
            END AS ExemplaireDispo,
            CASE
                WHEN emprunt.exemplaire_id IS NULL THEN 'present'
                WHEN emprunt.date_retour IS NULL THEN 'absent'
                ELSE 'present'
            END AS present
        FROM exemplaire
        JOIN oeuvre ON exemplaire.oeuvre_id = oeuvre.id_oeuvre
        LEFT JOIN
            (SELECT exemplaire_id, MAX(date_retour) AS date_retour 
            FROM emprunt
            GROUP BY exemplaire_id
            ) emprunt ON exemplaire.id_exemplaire = emprunt.exemplaire_id
        WHERE oeuvre.id_oeuvre = %s
        GROUP BY exemplaire.id_exemplaire, exemplaire.etat, exemplaire.date_achat, exemplaire.prix, oeuvre.titre, oeuvre.id_oeuvre, oeuvre.date_parution
        ORDER BY present DESC;'''
        cursor.execute(sql,(id_oeuvre))
        return cursor.fetchall()
    except ValueError:
        abort(400,'erreur requete 4_2')

def find_exemplaire_nbEmprunts(id):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete4_7' FROM DUAL '''
        sql = '''
        SELECT COUNT(*) as nb_emprunts FROM emprunt
        WHERE exemplaire_id = %s AND date_retour IS NULL;
        '''
        cursor.execute(sql, (id))
        res_nb_emprunts = cursor.fetchone()
        if 'nb_emprunts' in res_nb_emprunts.keys():
            nb_emprunts=res_nb_emprunts['nb_emprunts']
            return nb_emprunts
    except ValueError:
        abort(400,'erreur requete 4_7')

def find_edit_one_exemplaire(id):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete4_11' FROM DUAL '''
        sql = '''
        SELECT *, date_achat AS dateAchat 
        FROM exemplaire
        WHERE id_exemplaire = %s'''
        cursor.execute(sql, (id))
        return cursor.fetchone()
    except ValueError:
        abort(400,'erreur requete 4_11')

def find_id_oeuvre_exemplaire(id):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete4_9' FROM DUAL '''
        sql = '''
        SELECT oeuvre_id 
        FROM exemplaire
        WHERE id_exemplaire = %s'''
        cursor.execute(sql, (id))
        oeuvre = cursor.fetchone()
        oeuvre_id=str(oeuvre['oeuvre_id'])
        return oeuvre_id
    except ValueError:
        abort(400,'erreur requete 4_9')

def find_add_exemplaire_info_oeuvre(id):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete4_3' FROM DUAL '''
        sql = '''
        SELECT auteur.nom as nom, oeuvre.titre, oeuvre.id_oeuvre as id_oeuvre, oeuvre.date_parution
        FROM oeuvre
        INNER JOIN auteur ON oeuvre.auteur_id = auteur.id_auteur
        WHERE oeuvre.id_oeuvre = %s;
        '''
        cursor.execute(sql, (id))
        oeuvre = cursor.fetchone()
        return oeuvre
    except ValueError:
        abort(400,'erreur requete 4_3')

def find_edit_details_oeuvre_id_exemplaire(id):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete4_10' FROM DUAL '''
        sql = '''
        SELECT auteur.nom, oeuvre.titre, oeuvre.date_parution, oeuvre.id_oeuvre
        FROM exemplaire
        INNER JOIN oeuvre ON exemplaire.oeuvre_id = oeuvre.id_oeuvre
        INNER JOIN auteur on oeuvre.auteur_id = auteur.id_auteur
        WHERE exemplaire.id_exemplaire = %s;'''
        cursor.execute(sql, (id))
        exemplaire = cursor.fetchone()
        return exemplaire
    except ValueError:
        abort(400,'erreur requete 4_10')


def exemplaire_insert(noOeuvre,etat,dateAchat,prix):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete4_5' FROM DUAL '''
        sql = '''
        INSERT INTO exemplaire(oeuvre_id,etat,date_achat,prix)VALUES(%s,%s,%s,%s)
        '''   
        cursor.execute(sql, (noOeuvre,etat,dateAchat,prix))
        connection.commit()
    except ValueError:
        abort(400,'erreur requete 4_5')

def exemplaire_update(noOeuvre, etat, dateAchat, prix, id_exemplaire):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete4_12' FROM DUAL '''
        sql = '''
        UPDATE exemplaire SET oeuvre_id = %s, etat =  %s, date_achat = %s, prix = %s
        WHERE id_exemplaire = %s'''
        cursor.execute(sql, (noOeuvre, etat, dateAchat, prix, id_exemplaire))
        connection.commit()
    except ValueError:
        abort(400,'erreur requete 4_12')

def exemplaire_delete(id):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete4_8' FROM DUAL '''
        sql = '''
        DELETE FROM exemplaire
        WHERE id_exemplaire = %s'''
        cursor.execute(sql, (id))
        connection.commit()
    except ValueError:
        abort(400,'erreur requete 4_8')

# def other_request(id):
#     connection = get_db()
#     try:
#         cursor = connection.cursor()
#         sql = '''SELECT 'requete_OTHER' FROM DUAL '''
#         cursor.execute(sql,(id))
#         oeuvre = cursor.fetchone()
#         return oeuvre
#     except ValueError:
#         abort(400,'erreur requete_OTHER')