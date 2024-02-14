import random
from django.db import transaction
from django.core.management.base import BaseCommand


from skladiste.models import Zaposlenik, Proizvod, Tip_Proizvoda, Jedinica_Mjere



class Command(BaseCommand):
    help="removes all data from database"
    @transaction.atomic
    def handle(self, *args, **kwargs):
        #remove old data
        try:
            self.stdout.write("Removing data....")
            models=[Proizvod,Zaposlenik , Tip_Proizvoda, Jedinica_Mjere]
            for m in models:
                m.objects.all().delete()
        except Exception as e:
            self.stderr.write("Error purging: " + str(e))


        
