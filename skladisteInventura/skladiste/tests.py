from django.test import TestCase, Client
from django.db.models.deletion import ProtectedError
from http import HTTPStatus
from skladiste.models import *
from skladiste.forms import ProductForm, CategoryForm, UnitsForm
from skladiste.factory import ProizvodTestFactory, ZaposlenikFactory, Tip_ProizvodaFactory, Jedinica_MjereFactory
import random
# Create your tests here.
#on product form save, check if appropriate user is set to zaposlenik field

def fillDBInstance():
    """
    this function generates test DB data
    """
    for i in range (5):
            zaposlenik=ZaposlenikFactory()
    for i in range (5):
            tip_proizvoda=Tip_ProizvodaFactory()
    for i in range (5):
            jedinica_mjere=Jedinica_MjereFactory()
    for i in range (5):
            proizvod=ProizvodTestFactory()

class CalculatedFieldsDatabaseTest(TestCase):
    """class which tests the calculated fields when saving database entries
    """
    def setUp(self):
        fillDBInstance()
            
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
            
    # add form tests (get, post ....)
    
class ProizvodFormTest(TestCase):
        """class which contains tests for forms
        """
        def setUp(self):
            fillDBInstance()
                
        def test_input_fields_after_passing_data(self):
            """
            form fields should be filled according to the proizvod instance passed in post
            """
            proizvod=Proizvod.objects.order_by('?').first()
            form=ProductForm(data={'naziv_proizvoda': proizvod.naziv_proizvoda, 'opis_proizvoda':proizvod.opis_proizvoda, 'jedinicna_cijena':proizvod.jedinicna_cijena, 'kolicina':proizvod.kolicina,'tip_proizvoda':proizvod.tip_proizvoda, 'jedinica_mjere':proizvod.jedinica_mjere })
            
            
            self.assertEqual(form['naziv_proizvoda'].value(), proizvod.naziv_proizvoda)
            
            self.assertEqual(form['opis_proizvoda'].value(), proizvod.opis_proizvoda)
            self.assertEqual(form['jedinicna_cijena'].value(), proizvod.jedinicna_cijena)
            self.assertEqual(form['kolicina'].value(), proizvod.kolicina)
            self.assertEqual(form['tip_proizvoda'].value(), proizvod.tip_proizvoda.pk)
            self.assertEqual(form['jedinica_mjere'].value(), proizvod.jedinica_mjere.pk)
            
        def test_post_success(self):
            """after post to /novi_proizvod, the product should be accurately added to the DB (with all its fields)
            """
            self.user = User.objects.create_user(username='testuser', password='12345')

            productData={"naziv_proizvoda": "TEST", 'opis_proizvoda':"TESTNI OPIS", 'jedinicna_cijena':3295, 'kolicina':15,'tip_proizvoda':3, 'jedinica_mjere':2 }
            
            self.client.login(username='testuser', password='12345')
            response = self.client.post("/novi_proizvod", data=productData)
            
            addedProduct=Proizvod.objects.get(naziv_proizvoda=productData["naziv_proizvoda"])
            
            self.assertEqual(addedProduct.naziv_proizvoda, productData["naziv_proizvoda"])
            
            self.assertEqual(addedProduct.opis_proizvoda, productData["opis_proizvoda"])
            
            self.assertEqual(addedProduct.jedinicna_cijena, productData["jedinicna_cijena"])
        
            self.assertEqual(addedProduct.kolicina, productData["kolicina"])
        
            self.assertEqual(addedProduct.tip_proizvoda, Tip_Proizvoda.objects.get(pk=addedProduct.tip_proizvoda.pk))
            
            self.assertEqual(addedProduct.jedinica_mjere, Jedinica_Mjere.objects.get(pk=addedProduct.jedinica_mjere.pk))
            
            self.assertEqual(addedProduct.zaposlenik, User.objects.get(username='testuser'))
            
            self.assertEqual(addedProduct.jedinicna_osnovica_pdv, (addedProduct.tip_proizvoda.iznos_pdv * addedProduct.jedinicna_cijena))
                            
            self.assertEqual(addedProduct.jedinicna_ukupna_cijena, addedProduct.jedinicna_osnovica_pdv+addedProduct.jedinicna_cijena) 
            
class ProizvodFilterTest(TestCase):
    """class which contains tests for  proizvod filter forms
    """
    
    productData=0
    
    addedProduct=0
    
    def setUp(self):
            fillDBInstance()
            
            self.user = User.objects.create_user(username='testuser', password='12345')

            productData={"naziv_proizvoda": "TEST", 'opis_proizvoda':"TESTNI OPIS", 'jedinicna_cijena':3295, 'kolicina':15,'tip_proizvoda':3, 'jedinica_mjere':2 }
            
            self.client.login(username='testuser', password='12345')
            self.response = self.client.post("/novi_proizvod", data=productData)
            
            addedProduct=Proizvod.objects.get(naziv_proizvoda="TEST")
    
    def test_product_filter(self):
        """tests whether all the fields of the product filter form give the same result when applying filter and querying from DB
        """
        requestData_name={'product_name': "TEST" }
        requestData_category={'product_category': 3 }
        requestData_qty={ 'product_qty':15 }
        requestData_only_user={ 'product_only_user': 'on' }
        
        self.client.login(username='testuser', password='12345')
        
        self.response=self.client.post("/proizvodi", data=requestData_name)
        self.assertEqual(list(self.response.context['proizvodi']), list(Proizvod.objects.filter(naziv_proizvoda=requestData_name['product_name'])))
        
        self.response=self.client.post("/proizvodi", data=requestData_category)
        self.assertEqual(list(self.response.context['proizvodi']), list(Proizvod.objects.filter( tip_proizvoda=Tip_Proizvoda.objects.get(pk= requestData_category['product_category']))))

        self.response=self.client.post("/proizvodi", data=requestData_qty)
        self.assertEqual(list(self.response.context['proizvodi']), list(Proizvod.objects.filter( kolicina = requestData_qty['product_qty'])))
        
        self.response=self.client.post("/proizvodi", data=requestData_only_user)
        self.assertEqual(list(self.response.context['proizvodi']), list(Proizvod.objects.filter( zaposlenik= User.objects.get(username='testuser'))))


class TipProizvodaTest(TestCase):
    
    def setUp(self):
        fillDBInstance()
        
        
    def test_input_fields_after_passing_data(self):
        """check whether the appropriate fields are filled when Product category instance is passed to the form
        """
        tip_proizvoda=Tip_Proizvoda.objects.order_by('?').first()
        form=CategoryForm(data={'naziv_tipa': tip_proizvoda.naziv_tipa, 'iznos_pdv':tip_proizvoda.iznos_pdv })
            
            
        self.assertEqual(form['naziv_tipa'].value(), tip_proizvoda.naziv_tipa)       
        self.assertEqual(form['iznos_pdv'].value(), tip_proizvoda.iznos_pdv)       
            
    
            
    def test_post_success(self):
            """check whether product category is accurately added to DB with post on /novi_tip
            """
       

            catData={"naziv_tipa": "TESTTIP", 'iznos_pdv':0.15 }
            
            self.client.login(username='testuser', password='12345')
            response = self.client.post("/novi_tip", data=catData)
            
            added=Tip_Proizvoda.objects.get(naziv_tipa=catData["naziv_tipa"])
            
            self.assertEqual(added.naziv_tipa, catData["naziv_tipa"])
            
            self.assertEqual(added.iznos_pdv, catData["iznos_pdv"])
    
    def test_delete_fail(self):
        """check if delete of product category fails when the category is referenced in a product
        """
        
        tip_proizvoda=Proizvod.objects.order_by('?').first().tip_proizvoda
        try:
            tip_proizvoda.delete()
           
        except ProtectedError as err:
            self.assertIsInstance(err,ProtectedError)
    
    def test_delete_success(self):
        """check if delete of product category is successful if the product category isnt referenced in product
        """
        tip_proizvoda=Tip_ProizvodaFactory()
        pk=tip_proizvoda.pk
        
        self.assertTrue(Tip_Proizvoda.objects.filter(pk=pk).exists())
        
        tip_proizvoda.delete()
        self.assertFalse(Tip_Proizvoda.objects.filter(pk=pk).exists())
            
        
class JedinicaMjereTest(TestCase):
    
    def setUp(self):
        fillDBInstance()
        
        
    def test_input_fields_after_passing_data(self):
            """check whether appropriate fields are populated when measurement unit is passed to update form
            """
            jedinica_mjere=Jedinica_Mjere.objects.order_by('?').first()
            form=UnitsForm(data={'naziv_jedinice': jedinica_mjere.naziv_jedinice })
            
            
            self.assertEqual(form['naziv_jedinice'].value(), jedinica_mjere.naziv_jedinice)       
            
    
            
    def test_post_success(self):
        
            """check if new unit is added to DB with post /nova_jedinica
            """

            unitData={'naziv_jedinice': "novaMjernaJedinica"}
            
            self.client.login(username='testuser', password='12345')
            response = self.client.post("/nova_jedinica", data=unitData)
            
            added=Jedinica_Mjere.objects.get(naziv_jedinice=unitData["naziv_jedinice"])
            
            self.assertEqual(added.naziv_jedinice, unitData['naziv_jedinice'])
            
            
    def test_delete_fail(self):
        """check if measurement unit delete from DB fails if the entry is referenced in a product
        """
        
        jedinica_mjere=Proizvod.objects.order_by('?').first().jedinica_mjere
        try:
            jedinica_mjere.delete()
           
        except ProtectedError as err:
            self.assertIsInstance(err,ProtectedError)
    
    def test_delete_success(self):
        """check whether the measurement unit delete is successful when the entry isnt referenced in a product
        """
        
        jedinica_mjere=Jedinica_MjereFactory()
        pk=jedinica_mjere.pk
        
        self.assertTrue(Jedinica_Mjere.objects.filter(pk=pk).exists())
        
        jedinica_mjere.delete()
        self.assertFalse(Jedinica_Mjere.objects.filter(pk=pk).exists())
            
            