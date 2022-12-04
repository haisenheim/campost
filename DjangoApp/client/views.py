from django.shortcuts import render,HttpResponseRedirect, redirect
from django.contrib.auth.models import User
from .forms import  ClientStore, CompteGestion,Login, AgenceForm,UtlisateurForm,ClientSearch,TransactionForm
from .models import  Client, Compte, Agence, Role, Region,Operation,Profil
from django.http import HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.urls import reverse
import datetime

#ClientRegistration,
#User,
# Create your views here.
#def add_show(request):
    #if request.method == 'POST':
       #fm = ClientRegistration(request.POST)
        #if fm.is_valid():
            #nm = fm.cleaned_data['name']
            #tl = fm.cleaned_data['telephone']
            #em = fm.cleaned_data['email']
            #pw = fm.cleaned_data['password']
            #reg = User(name = nm, telephone = tl, email = em, password = pw)
            #reg.save()
            #fm = ClientRegistration()
    #else:
        #fm = ClientRegistration()
    #return render(request, 'client/addandshow.html',{'form':fm})
#cette fonction permet d'ajouteret d'afficher les infos d'un client

def home(request):
        return render(request, 'home.html')
    
    
def connexion(request):
        return render(request, 'connexion.html')   


    
#def comptes_view(request):
 #   return HttpResponse('LES COMPTES')



def traiter_client(request):
    if request.method == 'POST':
        fm = ClientStore(request.POST)
        if fm.is_valid():
            nom = fm.cleaned_data['nom']
            pren = fm.cleaned_data['prenom']
            tel = fm.cleaned_data['telephone']
            adr = fm.cleaned_data['adresse']
            reg = Client(nom = nom, prenom = pren, telephone =tel , adresse = adr)
            reg.save()
            fm = ClientStore()
    else:
        fm = ClientStore()
    clien = Client.objects.all()
    return render(request, 'Clients/edit.html',{'form':fm, 'cli':clien})

#cette fonction permet de supprimer les donnes
def delete_data(request, id):
    if request.method == 'POST':
        pi = Client.objects.get(pk=id)
        pi.delete()
        return HttpResponseRedirect('/')
    
#cette fonction permet de supprimer les donnes
def show_client(request, id):
   # if request.method == 'POST':
    pi = Client.objects.get(pk=id)
       # pi.delete()
    return render(request, 'Clients/show.html',{'client':pi})   
    

def traiter_compte(request):
    if request.method == 'POST':
        fm = CompteGestion(request.POST)
        if fm.is_valid():
            num = fm.cleaned_data['numero de compte']
            cli = fm.cleaned_data['client']
            solde = fm.cleaned_data['solde']
            jr = fm.cleaned_data['date ouverture']
            cpt = Compte(numero_de_compte = num, client = cli, solde =solde , date_ouverture = jr)
            cpt.save()
            fm = CompteGestion()
    else:
        fm = CompteGestion()
    compt = Compte.objects.all()
    return render(request, 'Comptes/edite.html',{'form':fm, 'cpt':compt})

#cette fonction permet de supprimer les donnes
def delete_data(request, id):
    if request.method == 'POST':
        pi = Compte.objects.get(pk=id)
        pi.delete()
        return HttpResponseRedirect('/')
    
def login_user(request):
    error = False
    if request.method == "POST":
        form = Login(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes
            if user:  # Si l'objet renvoyé n'est pas None
                now = datetime.datetime.now()
                user.profil.connected_at = now
                user.profil.save()
                login(request, user)  # nous connectons l'utilisateur
                if user.profil.role.id==1:
                    return redirect('/super/dashboard')
                if user.profil.role.id==2:
                    return redirect('/receveur/dashboard')
                if user.profil.role.id==3:
                    return redirect('/agent/dashboard')
                
            else: # sinon une erreur sera affichée
                error = True
    else:
        form = Login()

    return render(request, 'Profil/login.html', locals()) 

def deconnexion(request):
    logout(request)
    return redirect(reverse(login_user))


# Les actions de l'admin

def admin_dashboard(request):
    #return redirect('/some/url/')
    user = current_user = request.user
    if current_user.profil.role.id==1:
        return render(request, 'Admin/dashboard.html',locals())
    else:    
        return redirect('/login')
    
def admin_parametres_agences(request):
    #return redirect('/some/url/')
    if request.method=='POST':
        form = AgenceForm(request.POST)
        if form.is_valid():
            nom = form.cleaned_data["nom"]
            region = form.cleaned_data["region"]
            agence = Agence(nom=nom,region=region)
            agence.save()
            return HttpResponseRedirect(request.path_info)   
    else:    
        current_user = request.user
        if current_user.profil.role.id==1:
            agences = Agence.objects.all()
            regions = Region.objects.all()
            form = AgenceForm()
            return render(request, 'Admin/Agences/index.html',{'agences':agences,'regions':regions,'form':form})
        else:    
            return redirect('/login')
    

#Je gere les comptes utilisateurs ici
def admin_parametres_utilisateurs(request):
    #return redirect('/some/url/')
    if request.method=='POST':
        form = UtlisateurForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            ag_id = form.data.get("agence")
            role_id = form.data.get("role")
            agence = Agence.objects.get(pk=ag_id)
            role = Role.objects.get(pk=role_id)
            password = form.cleaned_data["password"]
            email = form.cleaned_data["email"]
            utilisateur = User.objects.create_user(username, email, password)
            profil = Profil(user=utilisateur,role=role,agence=agence)
            profil.save()
            return HttpResponseRedirect(request.path_info)   
    else:    
        current_user = request.user
        if current_user.profil.role.id==1:
            utilisateurs = Profil.objects.all()
            agences = Agence.objects.all()
            roles = Role.objects.all()
            #form = Form()
            return render(request, 'Admin/Utilisateurs/index.html',{'agences':agences,'utilisateurs':utilisateurs,'roles':roles})
        else:    
            return redirect('/login')
    
#Je gere les comptes utilisateurs ici
def admin_clients(request):
    #return redirect('/some/url/')
    
    current_user = request.user
    if current_user.profil.role.id==1:
        clients = Client.objects.all()
        #form = Form()
        return render(request, 'Admin/Clients/index.html',{'clients':clients,})
    else:    
        return redirect('/login')
#Je gere les comptes utilisateurs ici
def admin_client(request,id):
    #return redirect('/some/url/')
    
    current_user = request.user
    if current_user.profil.role.id==1:
        client = Client.objects.get(pk=id)
        #form = Form()
        return render(request, 'Admin/Clients/show.html',{'client':client})
    else:    
        return redirect('/login')     
    
def admin_transactions(request):
    #return redirect('/some/url/')
    user = current_user = request.user
    if current_user.profil.role.id==1:
        transactions = Operation.objects.all()
        return render(request, 'Admin/transactions.html',{'transactions':transactions})
    else:    
        return redirect('/login')
    


#Liste des actions du receveur
#Je gere les comptes utilisateurs ici
def receveur_utilisateurs(request):
       
    current_user = request.user
    if current_user.profil.role.id==2:
        agence = current_user.profil.agence
        utilisateurs = Profil.objects.filter(agence=agence)
        return render(request, 'Receveur/Utilisateurs/index.html',{'utilisateurs':utilisateurs})
    else:    
        return redirect('/login')
    
def receveur_dashboard(request):
    current_user = request.user
    if current_user.profil.role.id==2:
        return render(request, 'Receveur/dashboard.html',locals())
    else:    
        return redirect('/login')
    
def receveur_transactions(request):
    current_user = request.user
    if current_user.profil.role.id==2:
        transactions = Operation.objects.filter(agence=current_user.profil.agence)
        return render(request, 'Receveur/transactions.html',{'transactions':transactions})
    else:    
        return redirect('/login') 

def agent_dashboard(request):
    current_user = request.user
    if current_user.profil.role.id==3:
        return render(request, 'Agent/dashboard.html',locals())
    else:    
        return redirect('/login')
    
def agent_transactions(request):
    current_user = request.user
    if current_user.profil.role.id==3:
        transactions = Operation.objects.filter(user=current_user)
        return render(request, 'Agent/transactions.html',{'transactions':transactions})
    else:    
        return redirect('/login')    
 
def agent_create_client(request):
    #return redirect('/some/url/')
    if request.method=='POST':
        form = ClientStore(request.POST, request.FILES)
        if form.is_valid():
            nom = form.cleaned_data["nom"]
            prenom = form.cleaned_data["prenom"]
            telephone = form.cleaned_data["telephone"]
            adresse = form.cleaned_data["adresse"]
            dtn = form.data.get("dtn")
            lieu = form.data.get("lieu")
            photo = form.data.get("photo")
            current_user = request.user
            agence = current_user.profil.agence
            now = datetime.datetime.now()
            numero = '{}{}{}'.format(now.strftime('%H%d%m%y'),agence.id,current_user.id)
            client = Client.objects.create(nom=nom,prenom=prenom,telephone=telephone,adresse=adresse,dtn=dtn,lieu=lieu,photo=photo,user=current_user,agence=agence)
            compte = Compte.objects.create(client=client,solde=0,numero=numero)
            return render(request, 'Agent/client.html',{'client':client})
        return HttpResponseRedirect(request.path_info)   
 
def agent_client(request):
    form = ClientSearch(request.POST)
    if form.is_valid():
        numero = form.cleaned_data["numero"]
        compte = Compte.objects.get(numero=numero)
        current_user = request.user
        if current_user.profil.role.id==3:
            return render(request, 'Agent/client.html',{'client':compte.client})
    else:    
        return redirect('/login')

def agent_depot(request):
    form = TransactionForm(request.POST)
    if form.is_valid():
        montant = form.data.get("montant")
        numero = form.data.get("numero")
        compte = Compte.objects.get(numero=numero)
        current_user = request.user
        if current_user.profil.id==3:
            now = datetime.datetime.now()
            num = '{}{}{}'.format(now.strftime('%H%d%m%y'),current_user.profil.agence.id,current_user.id)
            transaction = Operation.objects.create(montant=montant,compte=compte,client=compte.client,user=current_user,agence=current_user.profil.agence,region=current_user.profil.agence.region,autorisation=num)
            compte.solde = compte.solde + int(montant)
            compte.save()
            return redirect('/agent/transactions')
        else:    
            return redirect('/login')   
        
def agent_retrait(request):
    form = TransactionForm(request.POST)
    if form.is_valid():
        montant = form.data.get("montant")
        numero = form.data.get("numero")
        compte = Compte.objects.get(numero=numero)
        current_user = request.user
        if current_user.profil.role.id==3:
            now = datetime.datetime.now()
            num = '{}{}{}'.format(now.strftime('%H%d%m%y'),current_user.profil.agence.id,current_user.id)
            transaction = Operation.objects.create(montant=montant,compte=compte,client=compte.client,user=current_user,agence=current_user.profil.agence,is_deposit=False,region=current_user.profil.agence.region,autorisation=num)
            compte.solde = compte.solde - int(montant)
            compte.save()
            return redirect('/agent/transactions')
        else:    
            return redirect('/login')                  
       
   

# Generated by Django 4.1.2 on 2022-10-18 23:59

#from django.db import migrations, models


#class Migration(migrations.Migration):

 #   initial = True

  #  dependencies = [
   # ]

    #operations = [
     #   migrations.CreateModel(
      #      name='User',
       #     fields=[
        #        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
         #       ('name', models.CharField(max_length=70)),
          #      ('telephone', models.CharField(max_length=100)),
           #     ('email', models.CharField(max_length=100)),
            #    ('password', models.CharField(max_length=100)),
#            ],
 #       ),
  #  ]
 