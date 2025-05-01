from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Binder
from .forms import UserCardInfoForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .services import fetch_card_data

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('binder-index')
        else:
            error_message = 'Invalid sign up - try again'
            print(form.errors) 
    
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)



class Home(LoginView):
    template_name = 'binder/home.html'


class BinderList(LoginRequiredMixin, ListView):
    model = Binder
    template_name = 'binders/index.html'

class BinderCreate(LoginRequiredMixin, CreateView):
    model = Binder
    fields = ['name', 'description']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        self.object = form.save()
        return redirect('binder-detail', pk=self.object.pk)
    

class BinderDetail(LoginRequiredMixin, DetailView):
    model = Binder



def search_cards(request, binder_id):
    print("search_cards function is being called")
    
    query = request.GET.get('query') 
    cards = []  
    
    if query:
        query = query.strip()  
        data = fetch_card_data(query)
        
        if data and 'data' in data:
            for card in data['data']:
                cards.append({
                    'id': card['id'],
                    'name': card.get('name'),
                    'small_img': card.get('images', {}).get('small'),
                    'large_img': card.get('images', {}).get('large'),
                    'set_name': card.get('set', {}).get('name'),
                    'set_series': card.get('set', {}).get('series'),
                    'tcg_url': card.get('tcgplayer', {}).get('url')
                })
    
    binder = get_object_or_404(Binder, id=binder_id)
    
    return render(request, 'binder/search_cards.html', {
        'cards': cards,
        'query': query,
        'binder': binder 
    })

def add_card_to_binder(request, binder_id, card_id):
    binder = get_object_or_404(Binder, id=binder_id)

    if request.method == 'POST':
        form = UserCardInfoForm(request.POST)
        if form.is_valid():
            user_card = form.save(commit=False)
            user_card.owner = request.user
            user_card.binder = binder
            user_card.card_id = card_id  
            user_card.save()
            return redirect('binder-detail', pk=binder_id)
    else:
        form = UserCardInfoForm()

    return render(request, 'binder/add_card.html', {
        'form': form,
        'binder_id': binder_id,
        'card_id': card_id
    })