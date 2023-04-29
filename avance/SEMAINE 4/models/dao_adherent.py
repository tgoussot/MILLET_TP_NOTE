
from connexion_db import get_db
from flask import *

def find_adherents():
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete2_1' FROM DUAL '''
        sql = '''
        SELECT adherent.nom,
            adherent.adresse,
            DATE_FORMAT(adherent.date_paiement, '%d-%m-%Y') as date_paiement,
            adherent.id_adherent,
            COUNT(emprunt.date_emprunt) as nbr_emprunt,
            DATE_FORMAT(DATE_ADD(adherent.date_paiement, INTERVAL 1 YEAR), '%d-%m-%Y') as date_paiement_futur,
            IF(CURRENT_DATE() > DATE_ADD(adherent.date_paiement, INTERVAL 1 YEAR), 1, 0) as retard,
            IF(CURRENT_DATE() > DATE_ADD(adherent.date_paiement, INTERVAL 11 MONTH), 1, 0) as retardProche
        FROM adherent
        LEFT JOIN emprunt ON emprunt.adherent_id = adherent.id_adherent AND emprunt.date_retour IS NULL
        GROUP BY adherent.id_adherent
        ORDER BY adherent.nom ASC;
        '''        
        cursor.execute(sql)
        return cursor.fetchall()
    except ValueError:
        abort(400,'erreur requete 2_1')

def find_adherent_nbEmprunts(id):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete2_6' FROM DUAL '''
        sql = '''
        SELECT COUNT(*) as nb_emprunts FROM emprunt
        WHERE adherent_id = %s AND date_retour IS NULL;
        '''
        cursor.execute(sql, (id))
        res_nb_emprunts = cursor.fetchone()
        if 'nb_emprunts' in res_nb_emprunts.keys():
            nb_emprunts=res_nb_emprunts['nb_emprunts']
            return nb_emprunts
    except ValueError:
        abort(400,'erreur requete 2_6')

def find_one_adherent(id):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete2_4' FROM DUAL '''
        sql = '''
        SELECT * FROM adherent 
        WHERE id_adherent = %s'''
        cursor.execute(sql, (id))
        return cursor.fetchone()
    except ValueError:
        abort(400,'erreur requete')

def adherent_insert(nom,adresse,datePaiement):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete2_2' FROM DUAL '''
        sql = '''
        INSERT INTO adherent(nom,adresse,date_paiement) VALUES (%s,%s,%s)
        '''
        cursor.execute(sql, (nom,adresse,datePaiement))
        connection.commit()
    except ValueError:
        abort(400,'erreur requete 1_2')

def adherent_update(nom,adresse,datePaiement,id):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete2_5' FROM DUAL '''
        sql = '''
        UPDATE adherent SET nom = %s, adresse = %s, date_paiement = %s
        WHERE id_adherent = %s'''
        cursor.execute(sql, (nom,adresse,datePaiement,id))
        connection.commit()
    except ValueError:
        abort(400,'erreur requete 2_5')

def adherent_delete(id):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete2_3' FROM DUAL '''
        sql = '''
        DELETE FROM adherent WHERE id_adherent = %s
        '''
        cursor.execute(sql, (id))
        connection.commit()
    except ValueError:
        abort(400,'erreur requete 2_3')
