import factory
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from skladiste.models import Proizvod, Tip_Proizvoda, Jedinica_Mjere


class ZaposlenikFactory(DjangoModelFactory):
    """
    class which is responsible for creating a "user" instance in DB
    """
    class Meta:
        model=get_user_model()

    username=factory.Faker("word")
    email=factory.Faker("email")
    first_name=factory.Faker("first_name")
    last_name=factory.Faker("last_name")


class Tip_ProizvodaFactory(DjangoModelFactory):
        """
        class which is responsible for creating a "tip proizvoda" instance in DB
        """
        class Meta:
            model=Tip_Proizvoda

        naziv_tipa=factory.Faker("sentence", nb_words=2)
        iznos_pdv=factory.Faker("pyfloat", min_value=0.10, max_value=0.3)

class Jedinica_MjereFactory(DjangoModelFactory):
        """
        class which is responsible for creating a "jedinica mjere" instance in DB
        """

        class Meta:
            model=Jedinica_Mjere

        naziv_jedinice=factory.Faker("word", ext_word_list=['kg','g','l','m','komad', 'pakiranje'])
        

class ProizvodFactory(DjangoModelFactory):
        """
        class which is responsible for creating a "Proizvod" instance in DB
        """
        class Meta:
            model=Proizvod
        
        naziv_proizvoda=factory.Faker("sentence",nb_words=3)
        opis_proizvoda=factory.Faker("paragraph", nb_sentences=4)
        jedinicna_cijena=factory.Faker("random_int", min=15, max=23000)
        kolicina=factory.Faker("random_int", min=0, max=1000)

        zaposlenik=factory.Iterator(get_user_model().objects.all())
        tip_proizvoda=factory.Iterator(Tip_Proizvoda.objects.all())
        jedinica_mjere=factory.Iterator(Jedinica_Mjere.objects.all())

        jedinicna_osnovica_pdv=factory.LazyAttribute(lambda o: o.tip_proizvoda.iznos_pdv)
        jedinicna_ukupna_cijena=factory.LazyAttribute(lambda o: o.jedinicna_osnovica_pdv + o.jedinicna_cijena)
        
class ProizvodTestFactory(DjangoModelFactory):
        """
        class which is responsible for creating a "Proizvod" instance in test DB
        """
        class Meta:
            model=Proizvod
        
        naziv_proizvoda=factory.Faker("sentence",nb_words=3)
        opis_proizvoda=factory.Faker("paragraph", nb_sentences=4)
        jedinicna_cijena=factory.Faker("random_int", min=15, max=23000)
        kolicina=factory.Faker("random_int", min=0, max=1000)

        zaposlenik=factory.Iterator(get_user_model().objects.all())
        tip_proizvoda=factory.Iterator(Tip_Proizvoda.objects.all())
        jedinica_mjere=factory.Iterator(Jedinica_Mjere.objects.all())

        jedinicna_osnovica_pdv=factory.LazyAttribute(lambda o: 0)
        jedinicna_ukupna_cijena=factory.LazyAttribute(lambda o: 0)