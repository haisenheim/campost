"""campost URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('__debug__/', include('debug_toolbar.urls')),
    path('admin/', admin.site.urls),
    path('', views.home),
    path('connexion/', views.connexion),
    path('compte/', views.traiter_compte, name = "edite"),
    
    #path('',views.add_show, name = "addandshow"),
    path('client/',views.traiter_client, name = "edit"),
    #path('',views.traiter_compte, name = "edite"),
    path('login/', views.login_user),
    path('deconnexion/', views.deconnexion),
    path('delete/<int:id>/',views.delete_data, name = "deletedata"),
    path('client/show/<int:id>/',views.show_client, name = "show_client"),
    
    
    # Les liens de l'administrateur
    path('super/dashboard',views.admin_dashboard, name = "admin_dashboard"),
    path('super/transactions',views.admin_transactions, name = "admin_dashboard"),
    path('super/parametres/agences',views.admin_parametres_agences, name = "admin_parametres_agences"),
    path('super/parametres/utilisateurs',views.admin_parametres_utilisateurs, name = "admin_parametres_utilisateurs"),
    path('super/clients',views.admin_clients, name = "admin_clients"),
    path('super/client/show/<int:id>',views.admin_client, name = "admin_client"),
    
    #Les liens du Receveur
    path('receveur/dashboard',views.receveur_dashboard, name = "receveur_dashboard"),
    path('receveur/utilisateurs',views.receveur_utilisateurs, name = "receveur_parametres_utilisateurs"),
    path('receveur/transactions',views.receveur_transactions, name = "receveur_transactions"),
    #path('receveur/transactions',views.receveur_transactions, name = "receveur_dashboard"),
    
    #Les liens de l'agent
    path('agent/dashboard',views.agent_dashboard, name = "agent_dashboard"),
    path('agent/transactions',views.agent_transactions, name = "agent_transactions"),
    path('agent/client/create',views.agent_create_client, name = "agent_create_client"),
    path('agent/client/search',views.agent_client, name = "agent_client"),
    path('agent/depot',views.agent_depot, name = "agent_depot"),
    path('agent/retrait',views.agent_retrait, name = "agent_retrait"),
]   
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)