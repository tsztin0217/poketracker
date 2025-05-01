from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Binder, UserCardInfo
from .forms import UserCardInfoForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .services import fetch_card_data, get_card_details_from_api

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

    def get_queryset(self):
        return Binder.objects.filter(owner=self.request.user)


class BinderCreate(LoginRequiredMixin, CreateView):
    model = Binder
    fields = ['name', 'description']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        self.object = form.save()
        return redirect('binder-detail', pk=self.object.pk)

class BinderUpdate(LoginRequiredMixin, UpdateView):
    model = Binder
    fields = ['name', 'description']

class BinderDelete(LoginRequiredMixin, DeleteView):
    model = Binder
    success_url = '/binders/'


@login_required
def binder_detail(request, pk):
    binder = get_object_or_404(Binder, pk=pk, owner=request.user)
    cards_in_binder = UserCardInfo.objects.filter(owner=request.user, binder=binder)

    cards_with_details = []
    for user_card in cards_in_binder:
        card_data = get_card_details_from_api(user_card.card_id)
        if card_data:
            cards_with_details.append({
                'user_card': user_card,
                'card': card_data 
            })

    return render(request, 'binder/binder_detail.html', {
        'binder': binder,
        'cards_with_details': cards_with_details,
    })

@login_required
def search_cards(request, binder_id):
    print("search_cards function is being called")
    
    query = request.GET.get('query', '') 
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
    
    binder = get_object_or_404(Binder, id=binder_id, owner=request.user)
    
    return render(request, 'binder/search_cards.html', {
        'cards': cards,
        'query': query,
        'binder': binder 
    }) 

@login_required
def card_detail_view(request, binder_id, card_id):
    binder = get_object_or_404(Binder, id=binder_id, owner=request.user)
    card = get_card_details_from_api(card_id)
    return render(request, 'binder/card_detail.html', {
        'binder': binder,
        'card': card
    })

@login_required
def add_card_to_binder(request, binder_id, card_id):
    binder = get_object_or_404(Binder, id=binder_id, owner=request.user)
    card = get_card_details_from_api(card_id)

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
        'binder': binder,
        'card': card
    })

@login_required
def user_card_detail(request, pk):
    user_card = get_object_or_404(UserCardInfo, pk=pk, owner=request.user)
    card = get_card_details_from_api(user_card.card_id)
    binder = user_card.binder 
    return render(request, 'binder/user_card_detail.html', {
        'user_card': user_card,
        'binder': binder,
        'card': card
    })