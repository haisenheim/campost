from django.core import validators
from django import forms
#from .models import User
from .models import Client,Compte,Agence

#class ClientRegistration(forms.ModelForm):
 #   class Meta:
  #      model = User
   #     fields = ['name', 'telephone', 'email', 'password']
    #    widgets = {
    #       'name': forms.TextInput(attrs={'class': 'form-control'}),
    #        'telephone': forms.TextInput(attrs={'class': 'form-control'}),
    #       'email': forms.EmailInput(attrs={'class': 'form-control'}),
    #       'password': forms.PasswordInput(attrs={'class': 'form-control'}),
    #    }

class ClientStore(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'prenom', 'adresse', 'telephone']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control','placeholder':'Adresse physique du client'}),
            'dtn': forms.DateField(),
            'lieu': forms.CharField(),
            'photo':forms.ImageField(),
        }   
        
class CompteGestion(forms.ModelForm):
    class Meta:
        model = Compte
        fields = ['numero', 'client', 'solde']
        widgets = {
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'client': forms.Select(attrs={'class': 'form-control'}),
            'solde': forms.FloatField(),
        }
        
class Login(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=100,
                          widget=forms.TextInput(
                              attrs={'class': "form-control"}))
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={'class': "form-control"}))
    
class ClientSearch(forms.Form):
    numero = forms.CharField(label="Numero de compte", max_length=100)

class TransactionForm(forms.Form):
    numero = forms.CharField(label="Numero de compte", max_length=100) 
    montant = forms.IntegerField()   

class AgenceForm(forms.ModelForm):
    class Meta:
        model = Agence
        fields = ['nom', 'region']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'region': forms.Select(attrs={'class': 'form-control'}),
        }
        
class UtlisateurForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    email = forms.CharField(label="Adresse email", max_length=30, widget=forms.EmailInput)
    agence = forms.Select(attrs={'class': 'form-control'}),
    role = forms.Select(attrs={'class': 'form-control'}),
           
                