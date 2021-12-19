from django.contrib.messages.api import MessageFailure
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth

# Create your views here.


def index(request):
    return render(request, "backend/login_register.html")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        repassword = request.POST["repassword"]

        if username == "" or email == "" or password == "" or repassword == "":
            messages.info(request, "*กรุณสป้อนข้อมูลให้ครบให้ครบ")
            return redirect('member')
        else:
            if password == repassword:
                if User.objects.filter(username=username).exists():
                    messages.info(request, "username already exists")
                elif User.objects.filter(email=email).exists():
                    messages.info(request, "email already exists")
                else:
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password
                    )
                    user.save()
                    messages.info(request, "*create complete")

            else:
                messages.info(request, "password not match")

            return redirect('member')


def login(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return redirect("panel")
    else:
        messages.info(request, "not found")
        return redirect("member")


def logout(request):
    auth.logout(request)
    return redirect("member")
