from django.shortcuts import render, render
from .models import *

def index(request):
    context = {}
    context['categories'] = Categories.objects.all()
    return render(request,'vimbiso/home.html',context)

def categories(request):
    context = {}
    context['categories'] = Categories.objects.all()
    return render(request,'vimbiso/categories.html',context)

def plans(request):
    return render(request,'vimbiso/plans.html')

def business(request):
    return render(request,'vimbiso/business_profile.html')

