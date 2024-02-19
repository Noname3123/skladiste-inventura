from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
# Create your models here.






class Jedinica_Mjere(models.Model):
    naziv_jedinice=models.CharField(max_length=100)

    def __str__(self):
        return self.naziv_jedinice
    

class Tip_Proizvoda(models.Model):
    naziv_tipa=models.CharField( max_length=100)
    iznos_pdv=models.FloatField()


    def save(self):
        """ 
            Overload of save method. Updates all products of this category after changing values. This is done due to the calculated fields of entity Proizvod
        """
        products=Proizvod.objects.filter(tip_proizvoda=self)
        for i in products:
            i.save()
        super(Tip_Proizvoda,self).save()

    def __str__(self):
        return self.naziv_tipa
    

class Proizvod(models.Model):
    naziv_proizvoda=models.CharField(max_length=100)
    opis_proizvoda=models.CharField(max_length=300)
    jedinicna_cijena=models.FloatField()
    kolicina=models.IntegerField()
    jedinicna_osnovica_pdv=models.FloatField()
    jedinicna_ukupna_cijena=models.FloatField()

    ##foreign keys
    zaposlenik=models.ForeignKey(get_user_model(), db_column="user",on_delete=models.PROTECT) #you cannot delete employee - which is handled by User auth model in Django, it will give ProtectedError (sublcass of django.db.IntegrityError)
    tip_proizvoda=models.ForeignKey(Tip_Proizvoda,on_delete=models.PROTECT) #you cannot delete employee, it will give ProtectedError (sublcass of django.db.IntegrityError)
    jedinica_mjere=models.ForeignKey(Jedinica_Mjere,on_delete=models.PROTECT) #you cannot delete employee, it will give ProtectedError (sublcass of django.db.IntegrityError)

    def save(self):
        """
        Overload of save method, it updates fields zaposlenik, jedinicna_osnovica_pdv and ukupna cijena 
        """
        self.jedinicna_osnovica_pdv=self.tip_proizvoda.iznos_pdv * self.jedinicna_cijena
        self.jedinicna_ukupna_cijena=self.jedinicna_cijena+self.jedinicna_osnovica_pdv
        super(Proizvod,self).save()

    def __str__(self):
        return self.naziv_proizvoda + "-" + self.opis_proizvoda
    





