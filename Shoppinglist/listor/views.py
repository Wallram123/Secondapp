from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .models import List, Item
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import UserRegisterForm
from django.contrib import messages

class AllaListor(LoginRequiredMixin,ListView):
    model=List
    template_name = 'listor/hem.html'
    context_object_name = 'listor'
    ordering = ['created_date']

class EnLista(LoginRequiredMixin,ListView):
    model=Item
    template_name = 'listor/lista.html'
    context_object_name = 'items'

    def get_queryset(self):
        return Item.objects.filter(list=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['listan'] = List.objects.filter(id=self.kwargs['pk'])
        return context
    
class NyLista(LoginRequiredMixin,CreateView):
    model = List
    fields = ['list_name']

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['status'] = {'status':'Ny'}
        return context
    

    def form_valid(self,form):
        form.instance.list_user=self.request.user 
        return super().form_valid(form)


class UppdateraLista(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = List
    fields = ['list_name']

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['status'] = {'status':'Uppdatera'}
        return context
    
    def test_func(self):
        lista=self.get_object()
        if self.request.user == lista.list_user:
            return True
        return False


class RaderaLista(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = List
    success_url = '/'

    def test_func(self):
            lista=self.get_object()
            if self.request.user == lista.list_user:
                return True
            return False
    
class NyVara(LoginRequiredMixin,CreateView):
    model = Item
    fields = ['item_name', 'amount']

    def form_valid(self,form):
        form.instance.list=get_object_or_404(List,id=self.kwargs.get('pk'))
        return super().form_valid(form)
    

    
class UppdateraVara(LoginRequiredMixin,UpdateView):
    model = Item
    fields = ['list_name','amount']

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['status'] = {'status':'Uppdatera'}
        return context


class RaderaVara(LoginRequiredMixin,DeleteView):
    model = Item

    def get_succss_url(self):
        lista = self.object.list
        return reverse_lazy('lista-sida', kwargs={'pk':lista.id})
    
class RensaVaror(LoginRequiredMixin,UserPassesTestMixin, View):
    template_name = 'listor/confirm_delete_purchased.html'

    def get_success_url(self):
        lista = get_object_or_404(List, id=self.kwargs.get('pk'))
        return reverse_lazy('lista-sida', kwargs={'pk':lista.id})
    
    def test_func(self):
        user = self.request.user
        list_pk = self.kwargs['pk']
        lista = get_object_or_404(List, pk=list_pk) 
        return user == lista.list_user
    
    def get(self, request, *args, **kwargs):
        context={}
        list_pk = self.kwargs.get('pk')
        items_to_delete = Item.objects.filter(list_pk=list_pk, purchased=True)
        if not items_to_delete.exists():
            messages.warning(request, 'Det finns inga markerade varor att radera.')
            return HttpResponseRedirect(reverse_lazy('lista-sida', kwargs={'pk':list_pk}))
        
    def post(self, request, *args, **kwargs):

def registrera(request):
    if request.method == 'POST':
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            anvandarnamn = form.cleaned_data.get('username')
            messages.success(request,f'kinto skapades för {anvandarnamn}')
            return redirect('loggain')
    else:
        form=UserRegisterForm()
    return render(request, 'listor/registrera.html', {'form':form})