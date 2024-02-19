from django.shortcuts import render, redirect
from skladiste.forms import SignUpForm, UnitsForm, ProductForm, CategoryForm, ProductFilterForm
from skladiste.models import Proizvod, Tip_Proizvoda, Jedinica_Mjere
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.db.models import Q, ProtectedError
import operator
from functools import reduce
from django.contrib import messages
# Create your views here.

class HomePage(TemplateView):
    template_name="home.html"

class SignUpView(CreateView):
    form_class =SignUpForm
    success_url=reverse_lazy("login")
    template_name="registration/signup.html"


class ProizvodView(ListView):
    model=Proizvod
    template_name='lists/proizvodi_list.html'
    context_object_name='proizvodi'

    #list containing filters received from form
    filter_list=[]
    
    def get_queryset(self):
        query = super().get_queryset()
        if len(self.filter_list)>0:
            query=query.filter(reduce(operator.and_,self.filter_list))
            self.filter_list.clear()
        return query
     
    def get_context_data(self, **kwargs):
        context = super(ProizvodView, self).get_context_data(**kwargs)
        context['form'] = ProductFilterForm()
        return context       
    
    
    def get(self, request):
        """method called when get is called on view. It returns to home screen if user is not logged in
        """
        if not (request.user.is_authenticated):
            return redirect("home")
        
        else:
            return super().get(request=request)
    
    def post(self, request, *args, **kwargs):
        
        
        if request.POST.get('product_name',"")!="":
            self.filter_list.append(Q(naziv_proizvoda__icontains=request.POST['product_name']))
            
        if request.POST.get('product_qty', "")!="":
            self.filter_list.append(Q(kolicina=request.POST['product_qty']))
            
        if request.POST.get('product_category', "")!="":
            self.filter_list.append(Q(tip_proizvoda=request.POST['product_category']))
            
        if request.POST.get('product_only_user','off')=='on':
            self.filter_list.append(Q(zaposlenik=request.user))
        
        
        return render(request=request, template_name=self.template_name,context={'form':ProductFilterForm(request.POST), 'proizvodi': self.get_queryset()})

class TipProizvodaView(ListView):
    model=Tip_Proizvoda
    template_name='lists/kategorije_list.html'
    context_object_name='tipovi'

    def get(self, request):
        """method called when get is called on view. It returns to home screen if user is not logged in
        """
        if not (request.user.is_authenticated):
            return redirect("home")
        
        else:
            return super().get(request=request)


class JediniceMjereView(ListView):
    model=Jedinica_Mjere
    template_name='lists/jedinice_list.html'
    context_object_name='jedinice'

    def get(self, request):
        """method called when get is called on view. It returns to home screen if user is not logged in
        """
        if not (request.user.is_authenticated):
            return redirect("home")
        
        else:
            return super().get(request=request)


class ProizvodCreateView(CreateView):
    model=Proizvod
    form_class=ProductForm
    template_name="addEntries/create_proizvod.html"
    success_url=reverse_lazy('proizvodi')
    
    def get(self, request):
        """method called when get is called on view. It returns to home screen if user is not logged in
        """
        if not (request.user.is_authenticated):
            return redirect("home")
        
        else:
            return super().get(request=request)
    
    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.zaposlenik=request.user
            
            
            return super(ProizvodCreateView, self).form_valid(form)
        
        
        return render(request, self.template_name, {"form":form})
    
class ProizvodUpdateView(UpdateView):
    model=Proizvod
    form_class=ProductForm
    template_name="updateEntries/update_proizvod.html"
    success_url=reverse_lazy('proizvodi')
    canEdit=1 #is the user authorised to update entry, by default it is
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["canEdit"] =self.canEdit #add "variable" canEdit into context
        return context
    
    
    def get(self, request,pk):
        """method called when get is called on view. It returns to home screen if user is not logged in
        """
        if not (request.user.is_authenticated):
            return redirect("home")
        
        elif not (request.user==self.model.objects.get(pk=pk).zaposlenik): #if user selects entry of another user for edit
            self.canEdit=0 #user cannot edit
            return super().get(request=request)
        
        else:
            return super().get(request=request)
      
   
    
class ProizvodDeleteView(DeleteView):
    model=Proizvod
    template_name="deleteEntries/delete_proizvod.html"
    success_url=reverse_lazy('proizvodi')
    
    
    canEdit=1 #is the user authorised to update entry, by default it is
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["canEdit"] =self.canEdit #add "variable" canEdit into context
        return context
    
    
    def get(self, request,pk):
        """method called when get is called on view. It returns to home screen if user is not logged in
        """
        if not (request.user.is_authenticated):
            return redirect("home")
        
        elif not (request.user==self.model.objects.get(pk=pk).zaposlenik): #if user selects entry of another user for edit
            self.canEdit=0 #user cannot edit
            return super().get(request=request)
        
        else:
            return super().get(request=request)
        
      

    
class TipProizvodCreateView(CreateView):
    model=Tip_Proizvoda
    form_class=CategoryForm
    template_name="addEntries/create_tip.html"
    success_url=reverse_lazy('kategorije')
    
    def get(self, request):
        """method called when get is called on view. It returns to home screen if user is not logged in
        """
        if not (request.user.is_authenticated):
            return redirect("home")
        
        else:
            return super().get(request=request)
    
    
    
class TipProizvodUpdateView(UpdateView):
    model=Tip_Proizvoda
    form_class=CategoryForm
    template_name="updateEntries/update_tip.html"
    success_url=reverse_lazy('kategorije')
   
    
    
    def get(self, request,pk):
        """method called when get is called on view. It returns to home screen if user is not logged in
        """
        if not (request.user.is_authenticated):
            return redirect("home")
        
    
        else:
            return super().get(request=request)
      
   
    
class TipProizvodDeleteView(DeleteView):
    model=Tip_Proizvoda
    template_name="deleteEntries/delete_tip.html"
    success_url=reverse_lazy('kategorije')
    
    
    
    
    
    def get(self, request,pk):
        """method called when get is called on view. It returns to home screen if user is not logged in
        """
        if not (request.user.is_authenticated):
            return redirect("home")
        
        
        else:
            return super().get(request=request)
    
    def post(self, request,pk):
        
        try:
            return super().post(request=request)
        except ProtectedError as error:
            messages.error(request=request, message="Cannot delete entry because it is referenced in another table!")
            return render(request=request,template_name=self.template_name)
      
      
class MjeraCreateView(CreateView):
    model=Jedinica_Mjere
    form_class=UnitsForm
    template_name="addEntries/create_jedinica.html"
    success_url=reverse_lazy('jedinice_mjere')
    
    def get(self, request):
        """method called when get is called on view. It returns to home screen if user is not logged in
        """
        if not (request.user.is_authenticated):
            return redirect("home")
        
        else:
            return super().get(request=request)
    
    
class MjeraUpdateView(UpdateView):
    model=Jedinica_Mjere
    form_class=UnitsForm
    template_name="updateEntries/update_jedinica.html"
    success_url=reverse_lazy('jedinice_mjere')
   
    
    
    def get(self, request,pk):
        """method called when get is called on view. It returns to home screen if user is not logged in
        """
        if not (request.user.is_authenticated):
            return redirect("home")
        
    
        else:
            return super().get(request=request)
      
   
    
class MjeraDeleteView(DeleteView):
    model=Jedinica_Mjere
    template_name="deleteEntries/delete_jedinica.html"
    success_url=reverse_lazy('jedinice_mjere')
    
    
    
    
    
    def get(self, request,pk):
        """method called when get is called on view. It returns to home screen if user is not logged in
        """
        if not (request.user.is_authenticated):
            return redirect("home")
        
        
        else:
            return super().get(request=request)
      
    def post(self, request,pk):
        
        try:
            return super().post(request=request)
        except ProtectedError as error:
            messages.error(request=request, message="Cannot delete entry because it is referenced in another table!")
            return render(request=request,template_name=self.template_name)