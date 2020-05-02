from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth import logout, authenticate, login
from django.core import signing
from django.contrib import messages
from django.contrib.auth.models import User
from project24.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
import math
import random


def index(request):
    if request.user.is_authenticated:
        return redirect("home:index")
    else:
        return render(request, "auth/home1.html")


def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.success(
                request, f"{email} is not registered. Please try again.")
            return render(request, 'auth/login.html')
        if user.check_password(password):
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, "signed in successfully.")
            return redirect('auth:index')
        else:
            messages.success(request, "Wrong password. Please try again.")
            return render(request, 'auth/login.html')
    else:
        return render(request, 'auth/login.html')


def signout(request):
    logout(request)
    return redirect('auth:index')


def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        EMAIL = request.POST.get('email')
        password = request.POST.get('password')
        cnf_password = request.POST.get('confirm_password')
        if User.objects.filter(email=EMAIL).exists():
            messages.success(request, "This email is already registered.")
            resp = render(request, 'auth/register.html')
        else:
            if password == cnf_password:
                email = signing.dumps(EMAIL)
                password = signing.dumps(password)
                resp = redirect("auth:reg_email", name=name,
                                EMAIL=email, password=password)
            else:
                messages.success(
                    request, "password and confirm password does not match.")
                resp = render(request, 'auth/register.html')
    else:
        resp = render(request, 'auth/register.html')
    return resp


def varify_email(request, name, EMAIL, password):
    email = signing.loads(EMAIL)
    PASSWORD = signing.loads(password)
    if request.method != 'POST':
        # genetrating the otp
        number = request.POST.get("number")
        digits = "0123456789"
        OTP = ""
        for i in range(4):
            OTP += digits[math.floor(random.random() * 10)]
        # sending otp to email
        send_mail(
            'Reset password | varify your email',
            f'otp: {OTP}, please enter the exact 4 digit otp to varify your email.',
            EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        messages.success(request, "otp sent successfully.")
        # rendering the template
        resp = render(request, 'auth/varify_email.html', {"email": email})
        # saving the otp in a cookies to validate it
        resp.set_signed_cookie('otp', OTP)
        return resp
    else:
        # when data is submitted
        otp = request.POST.get("number")
        # validating the otp
        if otp == request.get_signed_cookie('otp'):
            # creating the user
            try:
                user = User.objects.create_user(email, email, password)
                user.first_name = name
                user.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')   
                return redirect("auth:index")
            ## IntegrityError ~~ user is already created.
            except IntegrityError:
                return HttpResponse("holy crap user already exists. Try signing in.")
        else:
            messages.success(request, "wrong otp.")
            return render(request, "auth/varify_email.html", {'email': email})


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            Email = signing.dumps(email)
            return redirect("auth:rpass", email=Email)
        else:
            messages.success(
                request, f"{email} is not registered to filmstream.")
            return render(request, "auth/fp.html")
    else:
        return render(request, "auth/fp.html")


def reset_password(request, email):
    Email = signing.loads(email)
    if request.method != "POST":
        digits = "0123456789"
        OTP = ""
        for i in range(4):
            OTP += digits[math.floor(random.random() * 10)]
        send_mail(
            'Reset password | varify your email',
            f'otp: {OTP}, please enter the exact 4 digit otp to varify your email.',
            EMAIL_HOST_USER,
            [Email],
            fail_silently=False,
        )
        # OTP generated is a string
        messages.success(
            request, f"Varification code successfully sent to {Email}.")
        resp = render(request, 'auth/resetotp.html', {"email": Email})
        resp.set_signed_cookie('otp', OTP)
        return resp
    else:
        otp = request.POST.get('otp')
        if otp == request.get_signed_cookie('otp'):
            return redirect("auth:cpass", email=email)
        else:
            messages.success(request, "wrong otp. please try again.")
            return render(request, 'auth/resetotp.html', {"email": Email})


def create_a_new_passwword(request, email):
    email = signing.loads(email)
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('cnf_password')
        if password == confirm_password:
            u = get_object_or_404(User, email=email)
            u.set_password(password)
            u.save()
            messages.success(
                request, "password changed successfully. Please login to continue")
            return redirect("auth:login")
        else:
            messages.success(
                request, "password and confirm password does not match. Please try again.")
            return render(request, "auth/create_password.html", {"email": email})
    else:
        return render(request, "auth/create_password.html")

