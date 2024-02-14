from django.contrib import admin
from skladiste.models import  Proizvod, Tip_Proizvoda, Jedinica_Mjere

# Register your models here.
to_register=[ Proizvod, Tip_Proizvoda, Jedinica_Mjere]

admin.site.register(to_register)