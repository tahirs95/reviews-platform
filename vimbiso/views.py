from django.contrib import messages
from django.shortcuts import redirect, render, render
from .models import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
import stripe
from django.urls import reverse
from django.db.models import Q
import json
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.utils.timezone import make_aware


@csrf_exempt
def webhook_received(request):
    webhook_secret = 'whsec_d1iEXsbQ0s9KEotUxCRIk35TxTOjkrlO'
    request_data = json.loads(request.body)

    if webhook_secret:
        # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
        signature = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload=request.body, sig_header=signature, secret=webhook_secret)
            data = event['data']
        except Exception as e:
            return e
        # Get the type of webhook event sent - used to check the status of PaymentIntents.
        event_type = event['type']
    else:
        data = request_data['data']
        event_type = request_data['type']
    data_object = data['object']

    if event_type == 'checkout.session.completed':
        print('checkout.session.completed')
           
    elif event_type == 'invoice.paid':
        print(data)
        response = data['object']
        GetUser = User.objects.get(email=response['customer_email'])
        amount_received = response['total']/100
        if amount_received == 200:
            plan = 'Standard Plan ($200 per month)'
        elif amount_received == 500:
            plan = 'Premium Plan ($500 per month)'
            verified = True
        try:
            sub = Subscription.objects.get(user = GetUser)
            if verified:
                try:
                    GetUser.profile.verified = True
                except:
                    pass
            sub.sub_id = response['subscription']
            sub.is_active = True
            sub.period_start = make_aware(datetime.fromtimestamp(response['period_start']))
            sub.period_end = make_aware(datetime.fromtimestamp(response['period_end']))
            sub.amount_paid = amount_received
            sub.plan_type = plan
            sub.save()
        except Subscription.DoesNotExist:
            sub = Subscription.objects.create(user = GetUser)
            if verified:
                try:
                    GetUser.profile.verified = True
                except:
                    pass
            sub.sub_id = response['subscription']
            sub.is_active = True
            sub.period_start = make_aware(datetime.fromtimestamp(response['period_start']))
            sub.period_end = make_aware(datetime.fromtimestamp(response['period_end']))
            sub.amount_paid = amount_received
            sub.plan_type = plan
            sub.save()

    elif event_type == 'invoice.payment_failed':
      print('payment_failed')

    else:
      print('Unhandled event type {}'.format(event_type))

    return JsonResponse({'status': 'success'})


def index(request):
    context = {}
    context['categories'] = Category.objects.all()[:12]
    context['company'] = User.objects.filter(is_superuser=False)
    context['reviews'] = Reviews.objects.all().order_by('created_at')
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
            try:
                context['reviews'] = Reviews.objects.filter(company=getUser)
                avg_ratings = Reviews.objects.filter(company=getUser).aggregate(Avg('ratings')) or 0 
                context['avg_ratings'] = avg_ratings['ratings__avg']
                context['avg_ratings_range'] = range(int(avg_ratings['ratings__avg']))
            except:
                pass
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
                company = request.user,
                tag = x
            )
            print(obj)
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
        _company_category = request.GET.get('category',None)
        if _company_category:
            context['companies'] = User.objects.filter(is_superuser=False,level=1,profile__category=Category.objects.get(id=_company_category)).distinct()
            return render(request,'vimbiso/companies.html',context)
        else:
            context['companies'] = User.objects.filter(is_superuser=False,level=1)
            return render(request,'vimbiso/companies.html',context)
    else:
        context = {}
        obj = request.POST['search']
        context['companies'] = User.objects.filter(Q(username__icontains=obj) | Q(profile__category__name__icontains=obj) & Q(is_superuser=False) & Q(level=1))
        return render(request,'vimbiso/companies.html',context)

def company_description(request,id=None):
    if request.method == "GET":
        context = {}
        getUser = User.objects.get(id=id)
        context['c'] = getUser
        try:
            context['total_reviews'] = Reviews.objects.filter(company=getUser).count()
            context['excellent'] = Reviews.objects.filter(company=getUser,ratings__range=(4,5)).count()
            context['great'] = Reviews.objects.filter(company=getUser,ratings__range=(3,4)).count()
            context['average'] = Reviews.objects.filter(company=getUser,ratings__range=(2,3)).count()
            context['poor'] = Reviews.objects.filter(company=getUser,ratings__range=(1,2)).count()
            context['bad'] = Reviews.objects.filter(company=getUser,ratings__lte=1).count()
            context['reviews'] = Reviews.objects.filter(company=getUser)
            avg_ratings = Reviews.objects.filter(company=getUser).aggregate(Avg('ratings')) or 0
            context['avg_ratings'] = avg_ratings['ratings__avg']
            context['avg_ratings_range'] = range(int(avg_ratings['ratings__avg'])) 
        except:
            pass
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
            customer_email = f"{request.user.email}",
            line_items=[{
                'price': priceID,
                'quantity': 1,
            }],
        )

        # Redirect to the URL returned on the session
        return redirect(session.url, code=303)

def payment_success(request):
    return render(request,'vimbiso/payment_success.html')

def payment_cancel(request):
    return render(request,'vimbiso/payment_cancel.html')

def contactus(request):
    return render(request,'vimbiso/contactus.html')

@login_required
def response(request):
    data = {'success': False} 
    if request.method=='POST':
        _id = request.POST.get('id')
        _response = request.POST.get('response')
        print(_id)
        print(_response)
        if _id and _response:
            obj = Reviews.objects.get(
                id = _id
            )
            obj.response = _response
            obj.save()
            data['success'] = True
            data['msg'] = "Response added. Kindly reload page to view response!"
        else:
            data['success'] = False

    return JsonResponse(data)

def filter(request):
    if request.method == "GET":
        context = {}
        no_of_reviews = request.GET['numberofreviews']
        time_period = request.GET.get('timeperiod',None)
        print(time_period)
        print(no_of_reviews)
        if no_of_reviews and time_period:
            print(User.objects.annotate(number_of_reviews=Count('reviews',filter=Q(reviews__created_at__month__lte=time_period))).filter(is_superuser=False,number_of_reviews__lte=5,level=1))
            context['companies'] = User.objects.annotate(number_of_reviews=Count('reviews',filter=Q(reviews__created_at__month__lte=time_period))).filter(is_superuser=False,number_of_reviews__lte=5,level=1)      
        else:
            context['companies'] = User.objects.annotate(number_of_reviews=Count('reviews')).filter(is_superuser=False,number_of_reviews__lte=5,level=1)
        print(context['companies'])
        return render(request,'vimbiso/companies.html',context)