
from connexion_db import get_db
from flask import *

def find_oeuvres():
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete3_1' FROM DUAL '''
        sql = '''
        SELECT auteur.nom, oeuvre.titre, oeuvre.date_parution AS date_parution_iso, COALESCE(oeuvre.photo, '') as photo, COUNT(E1.id_exemplaire) AS nb_exemplaire,
            COUNT(E2.id_exemplaire) AS nb_exemp_dispo, 
            CONCAT(LPAD(CAST(DAY(oeuvre.date_parution) AS CHAR(2)), 2, '0'), '/', LPAD(CAST(MONTH(oeuvre.date_parution) AS CHAR(2)), 2, '0'), '/', YEAR(oeuvre.date_parution)) AS date_parution,
            oeuvre.id_oeuvre
        FROM oeuvre
        INNER JOIN auteur ON oeuvre.auteur_id = auteur.id_auteur
        LEFT JOIN exemplaire AS E1 ON oeuvre.id_oeuvre = E1.oeuvre_id
        LEFT JOIN exemplaire AS E2 ON E2.id_exemplaire = E1.id_exemplaire 
            AND E2.id_exemplaire NOT IN (SELECT emprunt.exemplaire_id FROM emprunt WHERE emprunt.date_retour IS NULL)    
        GROUP BY auteur.nom, oeuvre.titre, oeuvre.date_parution, oeuvre.photo
        ORDER BY auteur.nom, oeuvre.titre
        '''
        cursor.execute(sql)
        return cursor.fetchall()
    except ValueError:
        abort(400,'erreur requete 3_1')

def find_oeuvre_nbExemplaires(id):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete3_7' FROM DUAL '''
        sql = '''
        SELECT COUNT(*) as nb_exemplaires FROM exemplaire
        WHERE oeuvre_id = %s
        '''
        cursor.execute(sql, (id))
        res_nb_exemplaires = cursor.fetchone()
        if 'nb_exemplaires' in res_nb_exemplaires.keys():
            nb_exemplaires=res_nb_exemplaires['nb_exemplaires']
            return nb_exemplaires
    except ValueError:
        abort(400,'erreur requete 3_7')

def find_one_oeuvre(id):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete3_4' FROM DUAL '''
        sql = '''
        SELECT * 
        FROM oeuvre
        WHERE id_oeuvre = %s
        '''
        cursor.execute(sql, (id))
        return cursor.fetchone()
    except ValueError:
        abort(400,'erreur requete 3_4')

def oeuvre_insert(titre,dateParution,photo,idAuteur):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete3_2' FROM DUAL '''
        sql = '''
        INSERT INTO oeuvre(titre,date_parution,photo,auteur_id) VALUES (%s,%s,%s,%s)
        '''
        cursor.execute(sql, (titre,dateParution,photo,idAuteur))
        connection.commit()
    except ValueError:
        abort(400,'erreur requete 3_2')

def oeuvre_update(titre,idAuteur,dateParution,photo,id):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete3_5' FROM DUAL '''
        sql = '''
        UPDATE oeuvre SET titre = %s, auteur_id = %s, date_parution = %s, photo = %s
        WHERE id_oeuvre = %s'''
        cursor.execute(sql, (titre,idAuteur,dateParution,photo,id))
        connection.commit()
    except ValueError:
        abort(400,'erreur requete 3_5')

def oeuvre_delete(id):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete3_3' FROM DUAL '''
        sql = ''' DELETE FROM oeuvre WHERE id_oeuvre = %s'''
        cursor.execute(sql, (id))
        connection.commit()
    except ValueError:
        abort(400,'erreur requete 3_3')
