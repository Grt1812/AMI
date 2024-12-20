from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True, blank=False, null=False)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True, verbose_name=_('Image de profil'))
    # Ajoutez d'autres champs personnalisés si nécessaire

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Ou n'importe quel autre champ que vous voulez demander en plus de l'email.

    class Meta:
        swappable = 'AUTH_USER_MODEL'
        verbose_name = _('Utilisateur')
        verbose_name_plural = _('Utilisateurs')


class IoMts(models.Model):
    type_Iot = models.CharField(max_length=255, verbose_name="Type IoMt")
    date_heure = models.DateTimeField()
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
    statut = models.CharField(max_length=50)
    date_creation = models.DateTimeField(auto_now_add=True)
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

class Diagnostic(models.Model):
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE, verbose_name="Patient")
    docteur = models.ForeignKey(Docteur, on_delete=models.CASCADE, verbose_name="Docteur")
    description = models.TextField(verbose_name="Description du diagnostic")
    date_diagnostic = models.DateField(auto_now_add=True, verbose_name="Date du diagnostic")
    
    class Meta:
        verbose_name = "Diagnostic"
        verbose_name_plural = "Diagnostics"

class RendezVous(models.Model):
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE, verbose_name="Patient")
    docteur = models.ForeignKey(Docteur, on_delete=models.CASCADE, verbose_name="Docteur")
    date_rendezvous = models.DateTimeField(verbose_name="Date du rendez-vous")
    motif = models.CharField(max_length=255, verbose_name="Motif du rendez-vous")

    class Meta:
        verbose_name = "Rendez-vous"
        verbose_name_plural = "Rendez-vous"
        ordering = ["date_rendezvous"]

class Statistique(models.Model):
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE, verbose_name="Patient")
    date = models.DateField(auto_now_add=True, verbose_name="Date")
    valeur = models.FloatField(verbose_name="Valeur")

    class Meta:
        verbose_name = "Statistique"
        verbose_name_plural = "Statistiques"
        ordering = ["date"]
