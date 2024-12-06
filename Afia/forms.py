from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Patients,IoMts,Prelevement,Prediction, User
class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        strip= False,
        widget= forms.PasswordInput(attrs={"autocomplete": "new-password"})
    )
    password2 = forms.CharField(
        label="Password confirmation",
        strip= False,
        widget= forms.PasswordInput(attrs={"autocomplete": "new-password"})
    )
    class Meta(UserCreationForm):
        model = User
        fields = UserCreationForm.Meta.fields+("password1","password2")

    def save(self, commit=True):
            user = super().save(commit=False)
            user.nom = self.cleaned_data['nom']  # Enregistrez le nom de l'utilisateur
            if commit:
                user.save()
            return user  
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patients
        fields = '__all__'  # Ou spécifiez les champs à afficher
class IoMtsForm(forms.ModelForm):
    class Meta:
        model = IoMts
        fields = '__all__'        
        labels = {'type_Iot':'Type des objets connectés', 'patient':'Patient'}
class PrelevementForm(forms.ModelForm):
    class Meta:
        model = Prelevement
        fields = '__all__'
class PredictionForm(forms.ModelForm):
    class Meta:
        model = Prediction
        fields = ['valeur']