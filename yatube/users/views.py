from django.views.generic import CreateView, TemplateView

from django.urls import reverse_lazy

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'


class LoggedOut(TemplateView):
    template_name = 'users/logged_out.html'
