from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('',views.acceuil,name="acceuil"),
    path('login/check', views.login_check, name='login_check'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_page, name='logout'),
    path('connexion/', views.connexion, name='connexion'),
    path('Profil/', views.Profil_patient, name='profil'),
    path('session/message/<int:id>', views.chat, name='message'),
    path('session/', views.chat_session, name='session'),
    path('statistiques_patient/<int:patient_id>', views.statistiques_patient, name='statistique'),
    path('profil/enregistrer/', views.Profil_enregistrer, name='profil_enregistrer'),
    path('prelevement/<int:patient_id>',views.Prelevementdonnees,name='ma_sante'),
    path('dashboard/patients/', views.patients_view, name='patients'),
    path('prediction/<int:patient_id>/', views.Prediction, name='Prediction'),
    path('predict/', views.predict, name='predict'),
    path("predict/result", views.result),
]
