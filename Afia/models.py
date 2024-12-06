from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

class User(AbstractUser):
    class Meta:
        swappable = 'AUTH_USER_MODEL'
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

class IoMts(models.Model):
    type_Iot = models.CharField(max_length=255, verbose_name="Type IoMt")
    class Meta:
        verbose_name = "Objet connecté"
        verbose_name_plural = "Objets connectés"

    def __str__(self):
        return self.type_Iot

    def get_absolute_url(self):
        return reverse('Afia:IoMts')

class Personne(models.Model):
    nom = models.CharField(max_length=255, verbose_name="Nom")
    prenom = models.CharField(max_length=255, verbose_name="Prenom")
    sexe = models.CharField(max_length=1, choices=[('M', 'Masculin'), ('F', 'Feminin')], null=True, blank=True, verbose_name="Sexe")
    
    class Meta:
        verbose_name = 'Identité'
        verbose_name_plural = 'Identités'

class Docteur(models.Model):
    utilisateur_dr = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="Docteur")
    identite_dr = models.ForeignKey(Personne, related_name='identite_dr', on_delete=models.CASCADE, null=True, verbose_name='Identité')
    
    class Meta:
        verbose_name = 'Docteur'
        verbose_name_plural = 'Docteurs'

class Patients(models.Model):
    utilisateur_patient = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="Patient")
    identite_patient = models.ForeignKey(Personne, related_name='identite_patient', on_delete=models.CASCADE, null=True, verbose_name='Identité')
    date_naissance = models.DateField(verbose_name="Date de naissance")
    poids = models.FloatField(blank=True, verbose_name="Poids")
    taille = models.FloatField(blank=True, verbose_name="Taille")
    Iot = models.ForeignKey(IoMts, on_delete=models.CASCADE, verbose_name="Iot device")
    
    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"

    def get_absolute_url(self):
        return reverse('Afia:Patients')

class Prelevement(models.Model):
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE, verbose_name="Patient")
    date_heure = models.DateField(auto_now=True)
    saturation_O = models.FloatField(null=True, blank=True, verbose_name="Saturation en oxygène")
    pression_A = models.CharField(max_length=20, null=True, blank=True, verbose_name="Pression Arterielle")
    temperature = models.FloatField(verbose_name="Temperature")
    frequence_C = models.IntegerField(null=True, blank=True, verbose_name="Frequence Cardiaque")
    
    class Meta:
        verbose_name = "Prélevement"
        verbose_name_plural = "Prélevements"
        ordering = ["date_heure", "saturation_O", "pression_A", "frequence_C", "temperature"]

class Prediction(models.Model):
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE, verbose_name="Patient")
    date_heure = models.DateTimeField(auto_now=True)
    valeur = models.FloatField()
    prediction_modele = models.FloatField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Prediction"
        verbose_name_plural = "Predictions"
        ordering = ["patient", "date_heure"]

class Message(models.Model):
    patient_session = models.ForeignKey(Patients, related_name='patient_session', on_delete=models.CASCADE)
    docteur_session = models.ForeignKey(Docteur, related_name='patient_session', on_delete=models.CASCADE)
    message = models.TextField()
    from_patient = models.BooleanField(verbose_name='envoyer par le patient')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
