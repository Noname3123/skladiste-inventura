from django.test import TestCase
from skladiste.models import *
from skladiste.factory import ProizvodTestFactory, ZaposlenikFactory, Tip_ProizvodaFactory, Jedinica_MjereFactory
import random
# Create your tests here.
#on product form save, check if appropriate user is set to zaposlenik field

class CalculatedFieldsDatabaseTest(TestCase):
    """class which tests the calculated fields when saving database entries
    """
    def setUp(self):
        for i in range (5):
            zaposlenik=ZaposlenikFactory()
        for i in range (5):
            tip_proizvoda=Tip_ProizvodaFactory()
        for i in range (5):
            jedinica_mjere=Jedinica_MjereFactory()
        for i in range (5):
            proizvod=ProizvodTestFactory()
            
    def test_check_calculated_fields(self):
        """calculated fields in proizvod entry (osnovica pdv and ukupna cijena) are properly calculated
        """
        for i in Proizvod.objects.all():
            self.assertEqual(i.jedinicna_osnovica_pdv, (i.tip_proizvoda.iznos_pdv * i.jedinicna_cijena))                
            self.assertEqual(i.jedinicna_ukupna_cijena, i.jedinicna_osnovica_pdv+i.jedinicna_cijena) 
            
    def test_check_fields_update_after_category_change(self):
        """calculated fields in proizvod entry should change after iznos pdv changes in one tip_proizvoda"""
        
        for i in Tip_Proizvoda.objects.all():
            i.iznos_pdv=  random.random()
            i.save() 
            i.refresh_from_db()       
            for j in Proizvod.objects.filter(tip_proizvoda=i):
                self.assertEqual(j.jedinicna_osnovica_pdv, (i.iznos_pdv * j.jedinicna_cijena))                
                self.assertEqual(j.jedinicna_ukupna_cijena, j.jedinicna_osnovica_pdv+j.jedinicna_cijena) 
            
    