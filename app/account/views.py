from django.views import generic
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

from .forms import LoginForm
from .mixin import LogoutRequiredMixin

# Create your views here.
@method_decorator(never_cache, name='dispatch')
class Home(LoginRequiredMixin, generic.TemplateView):
    login_url = 'login'
    template_name = 'accounts/home.html'


# Login Page Handling
@method_decorator(never_cache, name='dispatch')
class Login(LogoutRequiredMixin, generic.View):
    def get(self, *args, **kwargs):
        form = LoginForm()
        context = {
            "form": form
        }
        return render(self.request, 'accounts/login.html', context)

    def post(self, *args, **kwargs):
        form = LoginForm(self.request.POST)

        if form.is_valid():
            user = authenticate(
                self.request,
                username = form.cleaned_data.get('username'),
                password = form.cleaned_data.get('password')
            )
            if user:
                login(self.request, user)
                return redirect('home')
            
            else:
                messages.warning(self.request, "Wrong credentials")
                return redirect('login')

        return render(self.request, 'accounts/login.html', {'form': form})


# Logout page handling
class Logout(generic.View):
    def get(self, *args, **kwargs):
        logout(self.request)
        return redirect('login')