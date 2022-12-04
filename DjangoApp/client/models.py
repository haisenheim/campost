from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#class User(models.Model):
 #   name =  models.CharField(max_length=70)
 #  telephone =  models.CharField(max_length=100)
 #   email =  models.CharField(max_length=100)
 #   password =  models.CharField(max_length=100)
    


class Role(models.Model):
    nom = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return "{}".format(self.nom)

class Region(models.Model):
    nom = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
     
    def __str__(self) -> str:
        return "{}".format(self.nom)    
    
class Agence(models.Model):
    region = models.ForeignKey(Region, null=True, on_delete=models.SET_NULL)
    nom = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return "{}".format(self.nom)
           

class Profil(models.Model):
    user = models.OneToOneField(User,null=True, on_delete=models.SET_NULL)  # La liaison OneToOne vers le modèle User
    role = models.ForeignKey(Role, null=True, on_delete=models.SET_NULL)  # La liaison OneToOne vers le modèle Role
    agence = models.ForeignKey(Agence, null=True, on_delete=models.SET_NULL)
    avatar = models.ImageField(null=True, blank=True, upload_to="avatars/")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    connected_at = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return "Profil de {0}".format(self.user.username) 
    
class Client(models.Model):
    nom = models.CharField(max_length=70)
    prenom = models.CharField(max_length=70)
    telephone = models.IntegerField(max_length=70)
    adresse = models.CharField(max_length=200)
    dtn=models.DateField(blank=True)
    lieu = models.CharField(max_length=200,blank=True, null=True)
    photo = models.ImageField(null=True, blank=True, upload_to="photos/")
    created_at = models.DateTimeField(auto_now_add=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True)
    agence = models.ForeignKey(Agence, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    
    def __str__(self) -> str:
        return "{} {}".format(self.nom,self.prenom)
    
class Compte(models.Model):
    client = models.OneToOneField(Client,null=True, on_delete=models.SET_NULL)
    numero = models.CharField(max_length=100)
    solde = models.FloatField(default=0,verbose_name=u"Solde initial du compte")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return "{}".format(self.numero)
        
    
class Operation(models.Model):
    client = models.ForeignKey(Client, null=True, on_delete=models.SET_NULL)
    compte = models.ForeignKey(Compte, null=True, on_delete=models.SET_NULL)
    montant =models.IntegerField(default=0)
    autorisation = models.CharField(max_length=100)
    is_deposit=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    region = models.ForeignKey(Region, null=True, on_delete=models.SET_NULL)
    agence = models.ForeignKey(Agence, null=True, on_delete=models.SET_NULL)          


   
   
     