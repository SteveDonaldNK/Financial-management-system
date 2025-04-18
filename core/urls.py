from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('transaction/ajouter/', views.ajouter_transaction, name='ajouter_transaction'),
    path('compte/ajouter/', views.ajouter_compte, name='ajouter_compte'),
    path('transaction/modifier/<int:transaction_id>/', views.modifier_transaction, name='modifier_transaction'),
    path('transaction/supprimer/<int:transaction_id>/', views.supprimer_transaction, name='supprimer_transaction'),
]


