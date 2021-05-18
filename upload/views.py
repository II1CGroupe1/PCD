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

# Create your views here.
res ={}
def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        if (uploaded_file):
            fs = FileSystemStorage()
            name = fs.save(uploaded_file.name,uploaded_file)
            # file is saved
            path =fs.url(name)

            res= extraction(path)
            print(type(res))

            return render(request, 'affichage.html',{"aff":res})

    return render(request, 'upload.html')

def affichage(request):


    return render(request, 'affichage.html',{"aff":res})