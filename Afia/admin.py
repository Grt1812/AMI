from django.contrib import admin
from .models import Patients,IoMts,Prelevement, Docteur, Personne,RendezVous,Diagnostic,Statistique


@admin.register(IoMts)
class IoMtAdmin(admin.ModelAdmin):
    list_display = ('type_Iot','date_heure')

@admin.register(Patients)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('identite_patient', 'date_naissance', 'poids', 'taille' , 'Iot','statut')

@admin.register(Docteur)
class DocteurAdmin(admin.ModelAdmin):
    list_display = ('identite_dr', )

@admin.register(Personne)
class PersonneAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'sexe')

@admin.register(Prelevement)
class PrelevementAdmin(admin.ModelAdmin):
    list_display = ("date_heure","saturation_O","pression_A","frequence_C","temperature")

@admin.register(Diagnostic)
class DiagnosticAdmin(admin.ModelAdmin):
    list_display = ('patient', 'docteur', 'description', 'date_diagnostic')


@admin.register(RendezVous)
class RendezVousAdmin(admin.ModelAdmin):
    list_display = ['patient','docteur','date_rendezvous','motif']

@admin.register(Statistique)
class StatistiqueAdmin(admin.ModelAdmin):
    list_display = ['patient','date','valeur']
