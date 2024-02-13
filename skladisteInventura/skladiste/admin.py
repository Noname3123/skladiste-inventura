from django.contrib import admin
from skladiste.models import Zaposlenik, Proizvod, Tip_Proizvoda, Jedinica_Mjere

# Register your models here.
to_register=[Zaposlenik, Proizvod, Tip_Proizvoda, Jedinica_Mjere]

admin.site.register(to_register)