from django.shortcuts import render
import pathlib
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
#the new importations
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import os
from testfinal import extraction


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'




