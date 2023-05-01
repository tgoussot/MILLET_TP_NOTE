#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import *
import re
import datetime
from connexion_db import get_db

def validator_exemplaire(data):
    mycursor = get_db().cursor()
    # id,etat,date_achat,prix,oeuvre_id
    valid = True
    errors = dict()

    if 'id' in data.keys():
        if not data['id'].isdecimal():
            errors['id'] = 'type id incorrect'
            valid = False

    if data['etat'] == '':
        # flash('Titre doit avoir au moins deux caractères')
        errors['etat'] = "Vous n'avez choisis aucun état"
        valid = False

    try:
        datetime.datetime.strptime(data['dateAchat'], '%d/%m/%Y')
    except ValueError:
        # flash("la Date n'est pas valide")
        errors['dateAchat'] = "la Date n'est pas valide format:%d/%m/%Y"
        valid = False
    else:
        data['dateAchat_us'] = datetime.datetime.strptime(data['dateAchat'], "%d/%m/%Y").strftime("%Y-%m-%d")

    try:
        float(data['prix'])
    except ValueError:
        # flash("Prix n'est pas valide")
        errors['prix'] = "le Prix n'est pas valide"
        valid = False

    return (valid, errors, data)