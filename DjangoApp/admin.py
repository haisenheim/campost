from django.contrib import admin
#from .models import User
from .models import Client, Compte
# Register your models here.
#@admin.register(User)
#class UserAdmin(admin.ModelAdmin):
    #list_display = ('id','name','telephone','email','password')

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('nom','prenom','adresse','telephone') 
    
@admin.register(Compte)
class CompteAdmin(admin.ModelAdmin):
    list_display = ('numero','client','solde')  
          
