import random
from django.db import transaction
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from skladiste.models import Proizvod, Tip_Proizvoda, Jedinica_Mjere

from skladiste.factory import ZaposlenikFactory, ProizvodFactory, Tip_ProizvodaFactory, Jedinica_MjereFactory

NUM_EMPLOYEE=10
NUM_PRODUCT=50
NUM_PRODUCT_CATEGORY=5
NUM_MEASURE_UNIT=6

class Command(BaseCommand):
    help="Generates test data for project skladiste-inventura"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        #remove old data
        self.stdout.write("Removing data....")
        models=[Proizvod , Tip_Proizvoda, Jedinica_Mjere]
        for m in models:
            m.objects.all().delete()

        get_user_model().objects.filter(is_staff=False).delete()


        #generate new data
        self.stdout.write("Generating...")
        try:
            for _ in range(NUM_EMPLOYEE):
                user=ZaposlenikFactory()
            
            for _ in range(NUM_PRODUCT_CATEGORY):
                kategorija_proizvoda=Tip_ProizvodaFactory()

            for _ in range(NUM_MEASURE_UNIT):
                jedinica_mjere=Jedinica_MjereFactory()

            for _ in range(NUM_PRODUCT):
                proizvod=ProizvodFactory()
            self.stdout.write("Data generated")
        except Exception as e:
            self.stderr("Error generating data: " + str(e))        

        
