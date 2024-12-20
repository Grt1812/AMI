from django.http import JsonResponse
from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from Afia.models import Patients, IoMts,Prelevement,Message, Personne, Docteur,Statistique,Prediction
from .forms import CustomUserCreationForm,PatientForm
from django.http import HttpResponseBadRequest
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
import plotly.express as px
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from django.utils import timezone

@login_required(login_url='connexion')
def acceuil(request):
    # Vérification de l'authentification de l'utilisateur
    if request.user.is_authenticated:
        user = request.user
        is_patient = None
        utilisateur = None

        # Recherche de l'utilisateur comme patient ou médecin
        patient = Patients.objects.filter(utilisateur_patient=user).first()
        docteur = Docteur.objects.filter(utilisateur_dr=user).first()

        # Vérifier si l'utilisateur est un patient ou un docteur
        if patient:
            is_patient = True
            utilisateur = patient
            # Rediriger le patient vers sa page dédiée (par exemple, tableau de bord patient)
            return redirect('patient_dashboard')  # Assurez-vous que cette route est définie dans urls.py
        elif docteur:
            is_patient = False
            utilisateur = docteur
            # Afficher la page d'accueil du médecin
            total_patients = Patients.objects.count()  # Total des patients
            new_patients = Patients.objects.filter(date_creation__gte=timezone.now()-timezone.timedelta(days=30)).count()  # Nouveaux patients du mois
            total_rdv_today = IoMts.objects.filter(date_heure__date=timezone.now().date()).count()  # RDV aujourd'hui
            critical_cases = Prelevement.objects.filter(patient__statut='Critique').count()  # Cas critiques

            # Rendre la page d'accueil du médecin avec les statistiques
            context = {
                'user': user,
                'is_patient': is_patient,
                'utilisateur': utilisateur,
                'total_patients': total_patients,
                'new_patients': new_patients,
                'total_rdv_today': total_rdv_today,
                'critical_cases': critical_cases
            }

            return render(request, 'Afia/home.html', context)  # Page d'accueil du médecin
        else:
            # Si l'utilisateur n'est ni médecin ni patient, rediriger vers la page de connexion
            return redirect('connexion')

    # Si l'utilisateur n'est pas authentifié, rediriger vers la page de connexion
    return redirect('connexion')


def login_check(request):
    if request.method == 'POST':
        username = request.POST.get('username') # Récupère l'email (maintenant username dans le formulaire)
        password = request.POST.get('password')

        if not username or not password:
            return HttpResponseBadRequest("Email et mot de passe requis")

        user = authenticate(request, username=username, password=password) #  Authentification avec l'email comme username

        if user:
            login(request, user)
            return redirect('acceuil')
        else:
            return render(request, 'Afia/home.html', {'error': 'Identifiants invalides'})
    else:
        return render(request, 'Afia/connexion.html') #affiche la page de connexion si la requête n'est pas POST

@login_required(login_url='connexion')
def logout_page(request):
    logout(request)
    return redirect('connexion')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() #Handles password hashing automatically.
            #You don't need to manually set password again.
            login(request, user) # Log in the user immediately after creation
            messages.success(request, 'Inscription réussie !') #Use Django messages
            return redirect('acceuil')
        else:
            messages.error(request, 'Erreur d\'inscription. Veuillez vérifier les informations saisies.') #Use Django messages
            return render(request, 'Afia/connexion.html', {'form': form})

    else: # GET request, show the form
        form = CustomUserCreationForm()
        return render(request, 'Afia/connexion.html', {'form': form, 'register_mode': True})


def connexion(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)  #Authenticate using email as username

        if user is not None:
            login(request, user)
            return redirect('acceuil')
        else:
            messages.error(request, 'Email ou mot de passe incorrect.') #Use Django messages
            form = CustomUserCreationForm()  #Re-instantiate the form
            return render(request, 'Afia/connexion.html', {'form': form, 'login_error': True})
    else: #GET request, show the form
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


def patients_view(request):
    # Récupérer la liste des patients
    patients = Patients.objects.select_related('identite_patient').all()

    # Gestion du formulaire d'ajout de patient
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patients')  # Redirection après ajout
    else:
        form = PatientForm()

    # Préparer les statistiques
    total_patients = patients.count()
    new_patients = patients.filter(date_creation__gte='2024-01-01').count()  # Exemples
    rdv_today = 12  # Exemple statique
    critical_cases = patients.filter(diagnostic='Critique').count()

    context = {
        'patients': patients,
        'form': form,
        'total_patients': total_patients,
        'new_patients': new_patients,
        'rdv_today': rdv_today,
        'critical_cases': critical_cases,
    }

    return render(request, 'Afia/patients.html', context)


def Prediction(request):
    return render(request, 'Prediction.html')

def statistiques_patient(request, patient_id):
    # Récupérer les données statistiques du patient
    statistiques = Statistique.objects.filter(patient_id=patient_id).order_by('date')
    dates = [stat.date for stat in statistiques]
    valeurs = [stat.valeur for stat in statistiques]

    # Générer le graphique avec Plotly
    fig = px.line(
        x=dates,
        y=valeurs,
        labels={'x': 'Date', 'y': 'Valeur'},
        title='Évolution de l\'état du patient'
    )

    # Convertir le graphique en HTML
    graph_html = fig.to_html(full_html=False)

    # Renvoyer les données et le graphique au template
    return render(request, 'statistic.html', {'graph_html': graph_html})


def predict(request):
    return render(request,'Afia/predict.html')

def result(request):
    data = pd.read_csv('data/hyper&diabete.csv')

    X = data.drop("Outcome", axis=1)
    Y =  data['Outcome']
    X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.2)

    model = LogisticRegression()
    model.fit(X_train,Y_train)

    val1 = float(str(request.GET['n1']))
    val2 = float(str(request.GET['n2']))
    val3 = float(str(request.GET['n3']))
    val4 = float(str(request.GET['n4']))
    val5 = float(str(request.GET['n5']))
    val6 = float(str(request.GET['n6']))
    val7 = float(str(request.GET['n7']))
    val8 = float(str(request.GET['n8']))
    val9 = float(str(request.GET['n9']))
    val10 = float(str(request.GET['n10']))
    val11 = float(str(request.GET['n11']))
    val12 = float(str(request.GET['n12']))
    val13 = float(str(request.GET['n13']))
    val14 = float(str(request.GET['n14']))

    pred = model.predict([[val1, val2, val3, val4, val5, val6, val7, val8, val9,val10,val11,val12,val13,val4]]) 

    result1 = ""
    if pred==[1]:
        result1 = "Positive"
    else:
        result1 = "Negative" 


    return render(request,'Afia/predict.html',{"result2":result1})

