from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Binder
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

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
            print(form.errors)  # Debugging print statement
    
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
        return redirect('binder_detail', pk=self.object.pk)
    

class BinderDetail(LoginRequiredMixin, DetailView):
    model = Binder