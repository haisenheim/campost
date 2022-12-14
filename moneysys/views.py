from django.shortcuts import render,HttpResponseRedirect, redirect
from django.contrib.auth.models import User
from .forms import  ClientStore, CompteGestion,Login, AgenceForm,UtlisateurForm,ClientSearch,TransactionForm
from .models import  Client, Compte, Agence, Role, Region,Operation,Profil
from django.http import HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.urls import reverse
import datetime
from faker import Faker
import random
import locale
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage
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
            user = authenticate(username=username, password=password)  # Nous v??rifions si les donn??es sont correctes
            if user:  # Si l'objet renvoy?? n'est pas None
                if user.profil.is_active:
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
                else:
                    logout(request)
                    messages.error(request,'Ce compte ??t?? bloqu??! Bien vouloir contacter un administrateur!')            
                    return render(request, 'Profil/login.html', locals())
            else: # sinon une erreur sera affich??e
                #error = True
                messages.warning(request,'Utilisateur inexistant ou mauvais de mot de passe! Bien vouloir contacter un administrateur pour toute v??rification!')
        else:
            return render(request, 'Profil/login.html', locals()) 
                    
    else:
        form = Login()

    return render(request, 'Profil/login.html', locals()) 

def deconnexion(request):
    logout(request)
    return redirect(reverse(login_user))


# Les actions de l'admin

def admin_dashboard(request):
    #return redirect('/some/url/')
    locale.setlocale(locale.LC_ALL, '')
    user = current_user = request.user
    now = datetime.datetime.now()
    year = now.strftime('%Y')
    #month = now.strftime('%m')
    clients = Client.objects.filter(created_at__year=year)
    nb_clients = clients.count()
    agents = Profil.objects.filter(role_id=3)
    nb_agents = agents.count()
    operations = Operation.objects.filter(is_active=True).filter(created_at__year=year)
    retraits = operations.filter(is_deposit=False)
    nb_retraits = retraits.count()
    pr = 0
    if operations.count() >0:
        pr = round(nb_retraits*100/operations.count(),2)
    mt_retraits = 0
    for r in retraits:
        mt_retraits = mt_retraits+r.montant
    depots = operations.filter(is_deposit=True)
    nb_depots = depots.count()
    pd = 0
    if operations.count() >0:
        pd = round(nb_depots * 100/operations.count(),2)
    mt_depots = 0
    for d in depots:
        mt_depots = mt_depots + d.montant
   # Departure_Date.objects.filter(created_at__year__gte=year,
    #                          created_at__month__gte=month,
   #                           created_at__year__lte=year,
    #                          created_at__month__lte=month)
    if current_user.profil.role.id==1:
        return render(request, 'Admin/dashboard.html',{'clients':nb_clients,'agents':nb_agents,'mr':f'{mt_retraits:n}','md':f'{mt_depots:n}','nb_r':nb_retraits,'nb_d':nb_depots,'pr':pr,'pd':pd})
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
    
def admin_delete_transaction(request,id):
    operation = Operation.objects.get(pk=id)
    current_user = request.user
    if current_user.profil.role.id==1:
        operation.is_active=False
        operation.save()
        compte = operation.compte
        if operation.is_deposit:
            compte.solde = compte.solde - operation.montant
        else:
             compte.solde = compte.solde + operation.montant
        compte.save()
        messages.info(request, "Annulation de l'op??ration effectu??e avec succes !")        
        return redirect('/super/transactions')
    else:    
        return redirect('/login')

def admin_disable_compte(request,id):
    client = Client.objects.get(pk=id)
    current_user = request.user
    if current_user.profil.role.id==1:
        compte = client.compte
        compte.is_active = False        
        compte.save()
        messages.info(request, "Compte Client bloqu?? avec succes !")        
        return redirect('/super/clients')
    else:    
        return redirect('/login')
    
def admin_enable_compte(request,id):
    client = Client.objects.get(pk=id)
    current_user = request.user
    if current_user.profil.role.id==1:
        compte = client.compte
        compte.is_active = True        
        compte.save()
        messages.success(request, "Compte Client r??activ?? avec succes !")        
        return redirect('/super/clients')
    else:    
        return redirect('/login') 
    
def admin_disable_user(request,id):
    user = Profil.objects.get(pk=id)
    current_user = request.user
    if (current_user.profil.role.id==1) & (user.id!=current_user.profil.id):
        user.is_active = False        
        user.save()
        messages.info(request, "Compte utilisateur bloqu?? avec succes !")                       
        return redirect('/super/parametres/utilisateurs')
    else:    
        return redirect('/login')
    
def admin_enable_user(request,id):
    user = Profil.objects.get(pk=id)
    current_user = request.user
    if current_user.profil.role.id==1:
        user.is_active = True        
        user.save()
        messages.success(request, "Compte utilisateur r??activ?? avec succes !")                        
        return redirect('/super/parametres/utilisateurs')
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
        transactions = Operation.objects.filter(is_active=True).all()
        return render(request, 'Admin/transactions.html',{'transactions':transactions})
    else:    
        return redirect('/login')
    
def admin_annulations(request):
    #return redirect('/some/url/')
    user = current_user = request.user
    if current_user.profil.role.id==1:
        transactions = Operation.objects.filter(is_active=False).all()
        return render(request, 'Admin/annulations.html',{'transactions':transactions})
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
    locale.setlocale(locale.LC_ALL, '')
   # user = current_user = request.user
    now = datetime.datetime.now()
    year = now.strftime('%Y')
    month = now.strftime('%m')
    clients = Client.objects.filter(created_at__year=year).filter(agence_id=current_user.profil.agence_id)
    nb_clients = clients.count()
    agents = Profil.objects.filter(role_id=3).filter(agence_id=current_user.profil.agence_id)
    nb_agents = agents.count()
    operations = Operation.objects.filter(created_at__year=year).filter(is_active=True).filter(created_at__month=month).filter(agence_id=current_user.profil.agence_id)
    retraits = operations.filter(is_deposit=False)
    nb_retraits = retraits.count()
    pr = 0
    if operations.count() >0:
        pr = round(nb_retraits*100/operations.count(),2)
    mt_retraits = 0
    for r in retraits:
        mt_retraits = mt_retraits+r.montant
    depots = operations.filter(is_deposit=True)
    nb_depots = depots.count()
    pd = 0
    if operations.count() >0:
        pd = round(nb_depots * 100/operations.count(),2)
    mt_depots = 0
    for d in depots:
        mt_depots = mt_depots + d.montant
   # Departure_Date.objects.filter(created_at__year__gte=year,
    #                          created_at__month__gte=month,
   #                           created_at__year__lte=year,
    #                          created_at__month__lte=month)
    if current_user.profil.role.id==2:
        return render(request, 'Receveur/dashboard.html',{'clients':nb_clients,'agents':nb_agents,'mr':f'{mt_retraits:n}','md':f'{mt_depots:n}','nb_r':nb_retraits,'nb_d':nb_depots,'pr':pr,'pd':pd})
    else:    
        return redirect('/login')
    
def receveur_transactions(request):
    current_user = request.user
    if current_user.profil.role.id==2:
        transactions = Operation.objects.filter(is_active=True).filter(agence=current_user.profil.agence)
        return render(request, 'Receveur/transactions.html',{'transactions':transactions})
    else:    
        return redirect('/login')
    
def receveur_disable_user(request,id):
    user = Profil.objects.get(pk=id)
    current_user = request.user
    if current_user.profil.role.id==2:
        if (user.agence==current_user.profil.agence) & (user.role.id==3):
            user.is_active = False        
            user.save()
            messages.info(request, "Compte utilisateur bloqu?? avec succes !")  
        else:
            messages.warning(request, "Impossible de bloquer ce compte utilisateur ! Vos droits sont limit??s sur ce dernier!")                      
        return redirect('/receveur/utilisateurs')
    else:    
        return redirect('/login')
    
def receveur_enable_user(request,id):
    user = Profil.objects.get(pk=id)
    current_user = request.user
    if current_user.profil.role.id==2:
        if (user.agence==current_user.profil.agence) & (user.role.id==3):
            user.is_active = True        
            user.save()
            messages.success(request, "Compte utilisateur reactiv?? avec succes !")  
        else:
            messages.warning(request, "Impossible de bloquer ce compte utilisateur ! Vos droits sont limit??s sur ce dernier!")                      
        return redirect('/receveur/utilisateurs')
    else:    
        return redirect('/login')     
    
def receveur_delete_transaction(request,id):
    operation = Operation.objects.get(pk=id)
    current_user = request.user
    if current_user.profil.role.id==2:
        if operation.agence==current_user.profil.agence:
            operation.is_active=False
            operation.save()
            compte = operation.compte
            if operation.is_deposit:
                compte.solde = compte.solde - operation.montant
            else:
                compte.solde = compte.solde + operation.montant
            compte.save()
            messages.info(request, "Annulation de l'op??ration effectu??e avec succes !")
        else:
            messages.warning(request, "Impossible d'annuler cette op??ration ! Vos droits sont limit??s sur cette op??ration!")            
        return redirect('/receveur/transactions')
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
            #photo = form.data.get("photo")
            current_user = request.user
            agence = current_user.profil.agence
            now = datetime.datetime.now()
            faker = Faker()
            numero = '{}{}{}'.format(now.strftime('%H%w%W%y%M%S'), f'{current_user.id:03}',random.randint(0, 9))
            #numero = faker.unique
            upload = request.FILES['upload']
            fss = FileSystemStorage()
            file = fss.save(numero, upload)
            file_url = fss.url(file)
            numero = '{}{}{}'.format(now.strftime('%H%w%W%y%M%S'), f'{current_user.id:03}',random.randint(0, 9))
            client = Client.objects.create(nom=nom,prenom=prenom,telephone=telephone,adresse=adresse,dtn=dtn,lieu=lieu,photo=file_url,user=current_user,agence=agence)
            compte = Compte.objects.create(client=client,solde=0,numero=numero)
            cr_date = datetime.datetime.strptime(client.dtn, '%Y-%m-%d')
            dtn = cr_date.strftime("%d-%m-%Y")
            return render(request, 'Agent/client.html',{'client':client,'dtn':dtn})
        return redirect('/agent/dashboard')  
 
def agent_client(request):
    form = ClientSearch(request.POST)
    if form.is_valid():
        numero = form.cleaned_data["numero"]
        try:
            compte = Compte.objects.get(numero=numero)
            current_user = request.user
            if current_user.profil.role.id==3:
                
                dtn = compte.client.dtn.strftime("%d-%m-%Y")
                return render(request, 'Agent/client.html',{'client':compte.client,'dtn':dtn})
        except ObjectDoesNotExist:
            messages.warning(request,'Attention! numero de compte inexistant!')
            return redirect('/agent/transactions')
    else:    
        return redirect('/login')

def agent_depot(request):
    form = TransactionForm(request.POST)
    if form.is_valid():
        montant = form.data.get("montant")
        numero = form.data.get("numero")
        compte = Compte.objects.get(numero=numero)
        current_user = request.user
        if current_user.profil.role.id==3:
           # print("profil role id :", current_user.profil.role.id)
           # return HttpResponse(f"Inside le if :  Le numero {numero} - le user {current_user.profil.role.id}")
            now = datetime.datetime.now()
            num = '{}{}{}'.format(now.strftime('%H%d%m%y'),current_user.profil.agence.id,current_user.id)
            Operation.objects.create(montant=montant,compte=compte,client=compte.client,user=current_user,agence=current_user.profil.agence,region=current_user.profil.agence.region,autorisation=num)
            
            compte.solde = compte.solde + int(montant)
            compte.save()
            messages.success(request, "Op??ration effectu??e avec succes !")
            return redirect('/agent/transactions')
        else: 
           # print("outside profil role id :", current_user.profil.role.id)
           # return HttpResponse(f"Outside le if :  Le numero {numero} - le user {current_user.profil.role.id == 3}")   
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
            mt = int(montant)
            if mt < compte.solde:
                transaction = Operation.objects.create(montant=montant,compte=compte,client=compte.client,user=current_user,agence=current_user.profil.agence,is_deposit=False,region=current_user.profil.agence.region,autorisation=num)
                compte.solde = compte.solde - int(montant)
                compte.save()
                messages.success(request, "Retrait effectu?? avec succes !")
            else:
                messages.error(request, "Echec de l'op??ration! Montant invalide !!!")    
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
 