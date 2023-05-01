#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from flask import *
import re
import datetime
from validator.validor_exemplaire_etu import * 
from models.dao_exemplaire import *

admin_exemplaire = Blueprint('admin_exemplaire', __name__,
                        template_folder='templates')

@admin_exemplaire.route('/admin/exemplaire/show')
def show_exemplaire():
    noOeuvre=request.args.get('id_oeuvre', '')

    sql = ''' SELECT 'requete4_1' FROM DUAL ''' 
    oeuvre = find_details_oeuvre_exemplaires(noOeuvre)
    
    sql = ''' SELECT 'requete4_2' FROM DUAL '''
    exemplaires = find_exemplaires_oeuvre(noOeuvre)

    return render_template('admin/exemplaire/show_exemplaires.html', exemplaires=exemplaires, oeuvre=oeuvre)

@admin_exemplaire.route('/admin/exemplaire/add', methods=['GET'])
def add_exemplaire():
    noOeuvre = request.args.get('id_oeuvre', '')

    sql = ''' SELECT 'requete4_3' FROM DUAL '''    
    oeuvre = find_add_exemplaire_info_oeuvre(noOeuvre)

    date_achat = datetime.datetime.now().strftime("%d/%m/%Y")
    return render_template('admin/exemplaire/add_exemplaire.html', oeuvre=oeuvre, donnees={'dateAchat': date_achat, 'noOeuvre': noOeuvre}, erreurs=[], date_achat = date_achat)

@admin_exemplaire.route('/admin/exemplaire/add', methods=['POST'])
def valid_add_exemplaire():
    noOeuvre = request.form.get('id_oeuvre','')
    dateAchat = request.form.get('date_achat', '')
    etat = request.form.get('etat', '')
    prix = request.form.get('prix', '')

    dto_data={'noOeuvre': noOeuvre, 'etat': etat, 'dateAchat': dateAchat, 'prix': prix}
    valid, errors, dto_data = validator_exemplaire(dto_data)

    if valid:
        dateAchat = dto_data['dateAchat_us']
        sql = ''' SELECT 'requete4_5' FROM DUAL '''
        exemplaire_insert(noOeuvre,etat,dateAchat,prix)

        message = u'exemplaire ajouté , oeuvre_id :'+str(noOeuvre)
        flash(message)
        
        return redirect('/admin/exemplaire/show?id_oeuvre='+str(noOeuvre))

    sql = ''' SELECT 'requete4_3' FROM DUAL '''
    oeuvre = find_add_exemplaire_info_oeuvre(noOeuvre)


    return render_template('admin/exemplaire/add_exemplaire.html', oeuvre=oeuvre, donnees=dto_data, erreurs=errors)

@admin_exemplaire.route('/admin/exemplaire/delete', methods=['GET'])
def delete_exemplaire():
    id = request.args.get('id_exemplaire', '') #id de l'exemplaire

    sql = '''SELECT 'requete4_9' FROM DUAL '''
    oeuvre_id=find_id_oeuvre_exemplaire(id)

    if not(id and id.isnumeric()):
        abort("404","erreur id oeuvre")

    nb_emprunts = 0
    sql = ''' SELECT 'requete4_7' FROM DUAL '''
    nb_emprunts = find_exemplaire_nbEmprunts(id)


    if nb_emprunts == 0 :
        sql = ''' SELECT 'requete4_8' FROM DUAL '''
        exemplaire_delete(id)

        # PAS COMPRIS
        
        # sql = ''' SELECT 'requete4_8' FROM DUAL '''
        # sql = '''
        # DELETE FROM oeuvre 
        # WHERE id_oeuvre = %s'''
        # mycursor.execute(sql, oeuvre_id)
        # flash(u'oeuvre supprimée, id: ' + id)

        flash(u'exemplaire supprimée, id: ' + id)

    else :
        flash(u'suppression impossible, il faut supprimer  : ' + str(nb_emprunts) + u' emprunt(s) de cet exemplaire')
    return redirect('/admin/exemplaire/show?id_oeuvre='+oeuvre_id)

@admin_exemplaire.route('/admin/exemplaire/edit', methods=['GET'])
def edit_exemplaire():
    id = request.args.get('id_exemplaire', '') #Exemplaire ID

    sql = ''' SELECT 'requete4_10' FROM DUAL ''' 
    oeuvre = find_edit_details_oeuvre_id_exemplaire(id)

    sql = ''' SELECT 'requete4_11' FROM DUAL '''
    exemplaire = find_edit_one_exemplaire(id)

    if exemplaire['dateAchat']:
        exemplaire['dateAchat']=exemplaire['dateAchat'].strftime("%d/%m/%Y")

    return render_template('admin/exemplaire/edit_exemplaire.html', exemplaire=exemplaire, oeuvre=oeuvre, erreurs=[])

@admin_exemplaire.route('/admin/exemplaire/edit', methods=['POST'])
def valid_edit_exemplaire():
    id_exemplaire = request.form.get('id_exemplaire', '')
    noOeuvre = request.form.get('oeuvre_id', '')
    dateAchat = request.form.get('dateAchat', '')
    etat = request.form.get('etat', '')
    prix = request.form.get('prix', '')

    dto_data={'oeuvre_id': noOeuvre, 'etat': etat, 'dateAchat': dateAchat, 'prix': prix, 'id_exemplaire':id_exemplaire}
    valid, errors, dto_data = validator_exemplaire(dto_data)

    if valid:
        dateAchat = dto_data['dateAchat_us']
        
        sql = ''' SELECT 'requete4_12' FROM DUAL '''
        exemplaire_update(noOeuvre, etat, dateAchat, prix, id_exemplaire)

        flash(u' exemplaire modifié, noOeuvre: ' + noOeuvre )
        return redirect('/admin/exemplaire/show?id_oeuvre='+noOeuvre)
    
    sql = ''' SELECT 'requete4_10' FROM DUAL '''
    oeuvre = find_edit_details_oeuvre_id_exemplaire(id_exemplaire)

    return render_template('admin/exemplaire/edit_exemplaire.html', exemplaire=dto_data, oeuvre=oeuvre, erreurs=errors)