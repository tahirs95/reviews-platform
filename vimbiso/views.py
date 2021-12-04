from django.contrib import messages
from django.shortcuts import redirect, render, render
from .models import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
import stripe
from django.urls import reverse

def index(request):
    context = {}
    context['categories'] = Category.objects.all()
    context['company'] = User.objects.all()
    return render(request,'vimbiso/home.html',context)

def categories(request):
    context = {}
    context['categories'] = Category.objects.all()
    return render(request,'vimbiso/categories.html',context)

@login_required
def plans(request):
    if request.method == "GET":
        return render(request,'vimbiso/plans.html')
    else:
        return redirect("vimbiso:plans")

@login_required
def business(request):
    if request.method=="GET":
        if request.user.is_authenticated and request.user.level==0:
            context = {}
            context['categories'] = Category.objects.all()
            return render(request,'vimbiso/complete_profile.html',context)
        else:
            context = {}
            getUser = request.user
            context['c'] = getUser
            context['reviews'] = Reviews.objects.filter(company=getUser)
            avg_ratings = Reviews.objects.filter(company=getUser).aggregate(Avg('ratings')) or 0 
            context['avg_ratings'] = avg_ratings['ratings__avg']
            context['avg_ratings_range'] = range(int(avg_ratings['ratings__avg']))
            return render(request,'vimbiso/business_profile.html',context)
    else:
        company_img = request.FILES['company-image']
        description = request.POST['description']
        tagsList = request.POST.getlist('tag')
        categoryID = request.POST.get('categories[]')
        print(f"{company_img},{description},{tagsList},{categoryID}")
        try:
            profile = BusinessProfile.objects.get(user=request.user)
        except BusinessProfile.DoesNotExist:
            profile = BusinessProfile.objects.create(user=request.user)
        profile.image = company_img
        profile.description = description
        profile.save()
        profile.category.add( Category.objects.get(id = categoryID) )
        for x in tagsList:
            obj = Tags.objects.create(
                company = request.user
            )
            obj.tag = x
            profile.tags.add(obj)
        request.user.level = 1
        request.user.save()
        return redirect("vimbiso:business")

def AddCategory(request):
    data = {'success': False} 
    if request.method=='POST':
        _name = request.POST.get('name')
        _parentid = request.POST.get('parent')

        if _parentid:
            Category.objects.create(
                name = _name,
                parent = Category.objects.get(id=_parentid)
            )
            data['msg'] = "Category created successfully. Kindly reload page to see the updated table"
            data['success'] = True
        else:
            Category.objects.create(
                name = _name,
            )
            data['msg'] = "Category created successfully. Kindly reload page to see the updated table"
            data['success'] = True

    return JsonResponse(data)

def aboutus(request):
    return render(request,'vimbiso/aboutus.html')

def addReview(request):
    if request.method=="POST":
        contact = request.POST['contact']
        name = request.POST['name']
        company = request.POST['company']
        purchased_item = request.POST['purchased-item']
        item_counter = request.POST['item-counter']
        date_of_purchase = request.POST['date']
        branch_location = request.POST['branch']
        review = request.POST['review']
        ratings = request.POST['rating']

        try:
            Reviews.objects.get(
                contact = contact,
                company = company
            )
            messages.error(request,"Your have already added review for that company!")
            return redirect("vimbiso:index")
        except Reviews.DoesNotExist:
            Reviews.objects.create(
                contact = contact,
                name = name,
                purchased_item = purchased_item,
                company = User.objects.get(id=company),
                item_counter = item_counter,
                date_of_purchase = date_of_purchase,
                branch_location = branch_location,
                review = review,
                ratings = ratings
            )
            messages.success(request,"Your review has been added successfully!")
            return redirect("vimbiso:index")


def companies(request):
    if request.method == "GET":
        context = {}
        context['companies'] = User.objects.filter(is_superuser=False)
        return render(request,'vimbiso/companies.html',context)

def company_description(request,id=None):
    if request.method == "GET":
        context = {}
        getUser = User.objects.get(id=id)
        context['c'] = getUser
        context['reviews'] = Reviews.objects.filter(company=getUser)
        avg_ratings = Reviews.objects.filter(company=getUser).aggregate(Avg('ratings')) or 0 
        context['avg_ratings'] = avg_ratings['ratings__avg']
        context['avg_ratings_range'] = range(int(avg_ratings['ratings__avg']))
        return render(request,'vimbiso/business_profile.html',context)

@login_required
def subscribe(request):
    if request.method == "POST":
        priceID = request.POST["price-id"]
        print(priceID)
        success = request.build_absolute_uri(reverse('vimbiso:payment_success'))
        cancel = request.build_absolute_uri(reverse('vimbiso:payment_cancel'))

        session = stripe.checkout.Session.create(
            success_url = success,
            cancel_url = cancel,
            mode='subscription',
            line_items=[{
                'price': priceID,
                'quantity': 1
            }],
        )

        # Redirect to the URL returned on the session
        return redirect(session.url, code=303)

def payment_success(request):
    return render(request,'vimbiso/payment_success.html')

def payment_cancel(request):
    return render(request,'vimbiso/payment_cancel.html')