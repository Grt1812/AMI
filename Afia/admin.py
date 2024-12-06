from django.contrib import admin
from .models import Patients,IoMts,Prelevement,Prediction, Docteur, Personne, Message


@admin.register(IoMts)
class IoMtAdmin(admin.ModelAdmin):
    list_display = ("type_Iot", )

@admin.register(Patients)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('identite_patient', 'date_naissance', 'poids', 'taille' , 'Iot')

@admin.register(Docteur)
class DocteurAdmin(admin.ModelAdmin):
    list_display = ('identite_dr', )

@admin.register(Personne)
class PersonneAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'sexe')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('patient_session', 'docteur_session', 'message', 'date', 'from_patient')

@admin.register(Prelevement)
class PrelevementAdmin(admin.ModelAdmin):
    list_display = ("date_heure","saturation_O","pression_A","frequence_C","temperature")

@admin.register(Prediction)
class predictionAdmin(admin.ModelAdmin):
    list_display = ['valeur']

