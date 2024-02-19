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

class ProductForm(forms.ModelForm):
    """
    Form responsible for adding new products into database
    """
    def __init__(self,*args, **kwargs):

        
        super(ProductForm, self).__init__(*args, **kwargs)

        self.fields['jedinicna_cijena'].widget.attrs['min'] = 0
        self.fields['kolicina'].widget.attrs['min'] = 0
        
        self.fields['jedinicna_cijena'].widget.attrs['max'] = 999999
        self.fields['kolicina'].widget.attrs['max'] = 999999
        
        self.fields['jedinicna_cijena'].initial = 0
        self.fields['kolicina'].initial = 0


    class Meta:
        model=Proizvod
        exclude=('jedinicna_osnovica_pdv', 'jedinicna_ukupna_cijena')
        fields=['naziv_proizvoda', 'opis_proizvoda', 'jedinicna_cijena','kolicina', 'tip_proizvoda', 'jedinica_mjere']
        
    tip_proizvoda= forms.ModelChoiceField(queryset = Tip_Proizvoda.objects.all())
    jedinica_mjere= forms.ModelChoiceField(queryset =Jedinica_Mjere.objects.all())
    
    
class CategoryForm(forms.ModelForm):
    """
    Form responsible for adding new categories (tip proizvoda) into database
    """
    def __init__(self,*args, **kwargs):

        
        super(CategoryForm, self).__init__(*args, **kwargs)

        self.fields['iznos_pdv'].widget.attrs['min'] = 0
        
        self.fields['iznos_pdv'].widget.attrs['max'] = 1
        
        self.fields['iznos_pdv'].initial = 0
        


    class Meta:
        model=Tip_Proizvoda
        fields=['naziv_tipa', 'iznos_pdv']
        
class UnitsForm(forms.ModelForm):
    """
    Form responsible for adding new measurement units into database
    """
    
        


    class Meta:
        model=Jedinica_Mjere
        fields=['naziv_jedinice']



class ProductFilterForm(forms.Form):
    """class which represents a form for filtering products
    """
    
    
    product_name=forms.CharField(label="Product Name", max_length=250, required=False)
    product_category=forms.ModelChoiceField(queryset=Tip_Proizvoda.objects.all(),label="Product Category", required=False)
    product_qty=forms.IntegerField(label="Product Quantity",required=False)
    product_only_user=forms.BooleanField(label="Show only products created by", required=False)