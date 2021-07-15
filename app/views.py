from django.shortcuts import get_object_or_404, render ,redirect
from account.forms import RegistrationForm
from account.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,authenticate,login
from django.contrib import auth
from django.contrib import messages
from .models import Category,Course,Profile
# Verification Email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage, message
import stripe
from datetime import datetime,timedelta
from django.urls import reverse
######################## REGISTER , VERIFICATION, LOGIN , LOGOUT  START ####################

stripe.api_key='sk_test_51JAExNCbKiyyexfdkXljLo7D1ujo55kqJngYWQkIbybPoqkM8O4Eo3F7ktiC67qrsnI5YStCWAokPfbN7YXlOPZa00T0UOKmav' #Pls write here your stripe secret keys


def register(request):
    if request.method=="POST":
        forms=RegistrationForm(request.POST)
        if forms.is_valid():
            email=forms.cleaned_data['email']
            first_name=forms.cleaned_data['first_name']
            last_name=forms.cleaned_data['last_name']
            password=forms.cleaned_data['password']
            confirm_password=forms.cleaned_data['confirm_password']
            username=email.split('@')[0]

            user=CustomUser.objects.create_user(email=email,first_name=first_name,last_name=last_name,username=username,password=password)
            user.save()
            current_site=get_current_site(request)
            mail_subject='Please active your account'
            message=render_to_string('verification.html',{
                'user' : user,
                'domain' : current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
            })
            to_email = email
            send_email= EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            return redirect("/login/?command=verification&email="+email)

    else:
        forms=RegistrationForm()

    return render(request, 'register.html',context={
        'forms' : forms
    })


def login(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        user=auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
            
        else:
            messages.error(request,'Invalid Login!')
            return redirect('register')
    
    return render(request, 'login.html',context={})




@login_required(login_url='register/')
def logout(request):
    auth.logout(request)
    return redirect('login')
    

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')

######################## REGISTER , VERIFICATION, LOGIN , LOGOUT  END ####################



@login_required(login_url='register/')
def home(request):
    courses=Course.objects.all()
    return render(request, 'home.html',context={
        'courses' : courses
    })

@login_required(login_url='register/')
def category(request,slug):
    category=get_object_or_404(Category,slug=slug)
    courses=category.category.all()
    return render(request, 'category.html',context={
        'courses' : courses
    })


@login_required(login_url='register/')
def course_detail(request,slug):
    course=Course.objects.get(slug=slug)
    return render(request, 'course_detail.html',context={
        'course' : course
    })

def premium(request):
    if request.method == "POST":
        membership= request.POST.get('membership','MONHTLY')
        amount = 10
        if membership == "YEARLY":
            amount = 100

        customer=stripe.Customer.create(
            email=request.user.email,
            source=request.POST['stripeToken']

        )
        charge=stripe.Charge.create(
            customer=customer,
            amount=amount*100,
            currency='usd',
            description= "Membership"
        )
        if charge['paid']==True:
            profile=Profile.objects.filter(user=request.user).first()
            if charge['amount'] == 1000:
                profile.subscription = "M"
                profile.is_pro=True
                expiry=datetime.now() + timedelta(30)
                profile.pro_expiry_date =expiry
                profile.save()
                current_site = get_current_site(request)
                mail_subject = 'Payment'
                message = render_to_string('verifi.html', {
                    'profile': profile,
                    'domain': current_site,
                    'amount' : amount,
                    'expiry' : expiry
            })
                to_email = request.user.email
                send_email = EmailMessage(mail_subject, message, to=[to_email])
                send_email.send()
            elif charge['amount'] == 10000:
                profile.subscription = "Y"
                profile.is_pro=True
                expiry= datetime.now()+timedelta(365)
                profile.pro_expiry_date=expiry
                profile.save()
            return redirect(reverse('charge'))

    return render(request, 'pro.html', context={})


def userpage(request):
    
    return render(request, 'userpage.html', context={})
    


def charge(request):
    return render(request, 'charge.html')
    