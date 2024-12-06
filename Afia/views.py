from django.http import JsonResponse
from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from Afia.models import Patients, IoMts, Prelevement,Prediction,Message, Personne, Docteur
from .forms import PatientForm, IoMtsForm, PrelevementForm, CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import logging
import os
import requests,json
from django.http import JsonResponse
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials 
from google.auth.exceptions import GoogleAuthError
#import tensorflow as tf
#import numpy as np


#from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

#def load_model():
   # model = tf.keras.models.load_model('model_AMI.h5')
    #return model

#def make_prediction(input_data):
    #model = load_model()
    #prediction = model.predict(input_data)
    #return prediction

@login_required(login_url='connexion')
def acceuil(request):
    if request.user.is_authenticated:
        user = request.user
        is_patient = existe = utilisateur = None
        patient = Patients.objects.filter(utilisateur_patient=user).first()
        dr = Docteur.objects.filter(utilisateur_dr=user).first()
        if patient:
            is_patient = True
            existe = True
            utilisateur = patient
        elif dr:
            is_patient = False
            existe = True
            utilisateur = dr
        else :
            is_patient = None
            existe = False
        patient = Patients.objects.filter(utilisateur_patient=user).first()
        if patient:
            patient_id = patient.id
        else:
            dr = Docteur.objects.filter(utilisateur_dr=user).first()
            patient_id = None
            if dr:
                patient = Patients.objects.order_by('?').first()
                patient_id = patient.id
        context = {
            'patient_id': patient_id, 
            'user': user,
            'existe': existe,
            'is_patient': is_patient,
            'utilisateur': utilisateur
        }
        #L'utilisateur est connecté
        return render(request, 'Afia/home.html', context=context)
    else:
        #L'utilisateur n'est pas connecté, redirigez-le vers la page de connexion
        
        return redirect('connexion')

def login_check(request):
    if request.method == 'POST':
        username = request.POST['username']
        pwd = request.POST['password']
        user = User.objects.filter(username=username).first()
        if user:
            auth_user = authenticate(request, username=username, password=pwd)
            if auth_user:
                login(request, user)
                return redirect('acceuil')
            else:
                #return render(request, 'Afia/connexion.html')
                return redirect('connexion')

@login_required(login_url='connexion')
def logout_page(request):
    logout(request)
    return redirect('connexion')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        pwd = request.POST['password']
        confirm = request.POST['confirm-password']
        if pwd == confirm:
            user = User(username=username, password=pwd)
            user.save()
            user.set_password(user.password)
            user.save()
            return redirect('connexion')

def connexion(request):
    form = CustomUserCreationForm() 
    return render(request, 'Afia/connexion.html', {'form': form}) 

@login_required(login_url='connexion')
def Profil_enregistrer(request):
    if request.method == 'POST':
        nom = request.POST.get('nom', '').strip()
        prenom = request.POST.get('prenom', '').strip()
        sexe = request.POST.get('sexe', '').strip()
        taille = request.POST.get('taille', '').strip()
        poids = request.POST.get('poids', '').strip()
        dn = request.POST.get('dob', '').strip()
        user = request.user

        # Validation des données
        if not nom or not prenom or not sexe or not taille or not poids or not dn:
            return render(request, 'profil.html', {'error': "Tous les champs sont obligatoires."})

        try:
            taille = int(taille)
            poids = int(poids)
            if taille <=0 or poids <=0:
                return render(request, 'profil.html', {'error': "Taille et poids doivent être des nombres positifs."})
            #Tentative de conversion en date et validation du format
            from datetime import datetime
            date_naissance = datetime.strptime(dn, '%Y-%m-%d').date() #'%Y-%m-%d' pour AAAA-MM-JJ. Adapter si besoin.

        except ValueError:
            return render(request, 'profil.html', {'error': "Format de date invalide. Veuillez utiliser AAAA-MM-JJ."})

        except Exception as e:
            return render(request, 'profil.html', {'error': f"Erreur: {str(e)}"})


        try:
            identite = Personne.objects.create(nom=nom, prenom=prenom, sexe=sexe)
            patient = Patients.objects.create(date_naissance=date_naissance, poids=poids, taille=taille, utilisateur_patient=user, identite_patient=identite)
            return redirect('acceuil')
        
        except ValidationError as e:
            return render(request, 'profil.html', {'error': f"Erreur de validation: {str(e)}"})
        except Exception as e:
            return render(request, 'profil.html', {'error': f"Erreur lors de l'enregistrement: {str(e)}"})
    
    return redirect('acceuil')

@login_required(login_url='connexion')
def Profil_patient(request):
    user = request.user
    patient = Patients.objects.filter(pk=user.id).first()
    if patient:
        return redirect('acceuil')
    else:
        return render(request, 'Afia/profil.html')


@login_required(login_url='connexion')
def Prelevementdonnees(request, patient_id):
    try:
        patient = Patients.objects.get(pk=patient_id)

        # Assurez-vous que vous avez configuré l'authentification avec Google
        creds = None
        token_file = 'path/to/your/token.json'

        # Charge les informations d'identification à partir du fichier token.json
        if os.path.exists(token_file):
            creds = Credentials.from_authorized_user_file(token_file, scopes=['https://www.googleapis.com/auth/fitness.heart_rate.read'])

        # Vérifiez si les informations d'identification sont valides
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                raise GoogleAuthError('Invalid Google Credentials')

        # Utilisation de l'API Google Health pour récupérer les données des capteurs
        url = 'https://www.googleapis.com/fitness/v1/users/me/dataSources/datasourceId/datasets/datasetId'
        headers = {
            'Authorization': f'Bearer {creds.token}',
            'Content-Type': 'application/json'
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Vérification du statut HTTP

        # Vérifiez si la réponse est bien au format JSON
        if response.headers['Content-Type'] == 'application/json':
            data = response.json()
            context = {
                'patient': patient,
                'heart_rate': data.get('heart_rate'),
                'blood_pressure': data.get('blood_pressure'),
                'oxygen': data.get('oxygen_saturation'),
                'temperature': data.get('temperature'),
            }
            return render(request, 'Afia/ma_sante.html', context)
        else:
            logging.error(f"La réponse du serveur n'est pas au format JSON: {response.text}")
            return JsonResponse({'error': 'Erreur de récupération des données'}, status=500)

    except Patients.DoesNotExist:
        return JsonResponse({'error': "Patient not found"}, status=404)
    except requests.exceptions.RequestException as e:
        logging.error(f"Erreur de requête HTTP: {e}")
        return JsonResponse({'error': str(e)}, status=500)
    except json.decoder.JSONDecodeError as e:
        logging.error(f"Erreur de décodage JSON: {e}")
        return JsonResponse({'error': 'Erreur de décodage JSON'}, status=500)
    except GoogleAuthError as e:
        logging.error(f"Erreur d'authentification Google: {e}")
        return JsonResponse({'error': 'Erreur d\'authentification Google'}, status=500)

@login_required(login_url='connexion')
def chat(request, id):
    try:
        messages = Message.objects.filter(docteur_session=Docteur.objects.get(pk=request.user.id)).filter(patient_session=Patients.objects.get(pk=id)).order_by('date').all()
    except:
        messages = []
    
    context = {
        'messages': messages,
        'user': request.user,
    }
    return render(request, 'Afia/chat.html', context)

@login_required(login_url='connexion')
def chat_session(request):
    try:
        boxes = [(i.patient_session.id, f'{i.patient_session.identite_patient.nom} {i.patient_session.identite_patient.prenom}')
            for i in Message.objects.filter(docteur_session=Docteur.objects.get(pk=request.user.id)).all()
        ]
        
        boxes = set(boxes)
    except:
        boxes = []
    
    context = {
        'boxes': boxes,
        'user': request.user,
    }
    return render(request, 'Afia/session_message.html', context)


def enregistrer_message(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        docteur_id = request.POST.get('docteur_id')
        message = request.POST.get('message')
        est_patient = request.POST.get('est_patient') == 'True'  # Convertir en booléen

        try:
            patient = Patients.objects.get(pk=patient_id)
            docteur = Docteur.objects.get(pk=docteur_id)

            message = Message.objects.create(
                patient=patient,
                docteur=docteur,
                message=message,
                est_patient=est_patient
            )
            message.save()

            return redirect('votre_url_de_redirection')  # Remplacez par l'URL de votre choix

        except (Patients.DoesNotExist, Docteur.DoesNotExist):
            return render(request, 'message_erreur.html')  # Remplacez par votre template d'erreur

    else:
        return render(request, 'Afia/chat.html')  # Remplacez par votre template de formulaire

def patient_detail_view(request, patient_id): 
    patient = get_object_or_404(Patients, id=patient_id) 
    prelevements = Prelevement.objects.filter(patient=patient).order_by('-date_heure') 
    context = { 
        'patient': patient, 
        'prelevements': prelevements, 
        } 
    return render(request, 'Afia/patient_detail.html', context)