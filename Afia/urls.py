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
    path('profil/enregistrer/', views.Profil_enregistrer, name='profil_enregistrer'),
    path('prelevement/<int:patient_id>',views.Prelevementdonnees,name='ma_sante'),
    path('patients/<int:patient_id>/', views.patient_detail_view, name='patient_detail'),
]
