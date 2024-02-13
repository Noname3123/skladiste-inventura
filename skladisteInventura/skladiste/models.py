from django.db import models

# Create your models here.


class Zaposlenik(models.Model):
    korisnicko_ime=models.CharField(max_length=200)
    ime_zaposlenika=models.CharField(max_length=50)
    prezime_zaposlenika=models.CharField(max_length=50)


    def __str__(self):
        return self.korisnicko_ime
    
class Jedinica_Mjere(models.Model):
    naziv_jedinice=models.CharField(max_length=100)

    def __str__(self):
        return self.naziv_jedinice
    

class Tip_Proizvoda(models.Model):
    naziv_tipa=models.CharField( max_length=100)
    iznos_pdv=models.FloatField()

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
    zaposlenik=models.ForeignKey(Zaposlenik,on_delete=models.PROTECT) #you cannot delete employee, it will give ProtectedError (sublcass of django.db.IntegrityError)
    tip_proizvoda=models.ForeignKey(Tip_Proizvoda,on_delete=models.PROTECT) #you cannot delete employee, it will give ProtectedError (sublcass of django.db.IntegrityError)
    jedinica_mjere=models.ForeignKey(Jedinica_Mjere,on_delete=models.PROTECT) #you cannot delete employee, it will give ProtectedError (sublcass of django.db.IntegrityError)


    def __str__(self):
        return self.naziv_proizvoda + "-" + self.opis_proizvoda
    





