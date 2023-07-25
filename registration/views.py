from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy, reverse
from django.contrib import messages

# Create your views here.

def sign_up(request):
    if request.user.is_authenticated:
        return reverse_lazy('homepage')
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('homepage')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

class SignInView(LoginView):
    redirect_authenticated_user = True
    template_name = 'registration/signin.html'
    def get_success_url(self):
        return reverse_lazy('homepage')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid password or login. Please, try again.')
        return self.render_to_response(self.get_context_data(form=form))