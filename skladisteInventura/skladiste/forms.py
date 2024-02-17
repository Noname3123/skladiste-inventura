from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from skladiste.models import Proizvod, Tip_Proizvoda, Jedinica_Mjere
from django.core.validators import MinValueValidator

class SignUpForm(UserCreationForm):
    """
    form responsible for registering a new user for app
    """
    class Meta:
        model=get_user_model()
        fields=('username','first_name', 'last_name', 'email','password1','password2')

class ProductAddForm(forms.ModelForm):
    """
    Form responsible for adding new products into database
    """
    def __init__(self,*args, **kwargs):

        
        super(ProductAddForm, self).__init__(*args, **kwargs)

        self.fields['jedinicna_cijena'].widget.attrs['min'] = 0
        self.fields['kolicina'].widget.attrs['min'] = 0


    class Meta:
        model=Proizvod
        exclude=('jedinicna_osnovica_pdv', 'jedinicna_ukupna_cijena')
        fields=['naziv_proizvoda', 'opis_proizvoda', 'jedinicna_cijena', 'zaposlenik','kolicina', 'tip_proizvoda', 'jedinica_mjere']
        
    tip_proizvoda= forms.ModelChoiceField(queryset = Tip_Proizvoda.objects.all())
    jedinica_mjere= forms.ModelChoiceField(queryset =Jedinica_Mjere.objects.all())
    