from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate
from django.core.handlers.wsgi import WSGIRequest


# Create your views here.
def regiseter(request: WSGIRequest):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        print(username)
        if not username or not email or not password:
            messages.warning(request, "กรุณาป้อนข้อมูลให้ครบถ้วน")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.warning(request, "อีเมลซ้ํา")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.warning(request, "ชื่อผู้ใช้ซ้ํา")
            return redirect("register")

        if len(password) < 4:
            messages.warning(request, "รหัสผ่านต้องมีความยาวอย่างน้อย 4 ตัวอักษร")
            return redirect("register")
        elif not any(char.isalpha() for char in password):
            messages.warning(request, "รหัสผ่านต้องมีอักษรอย่างน้อย 1 ตัวอักษร")
            return redirect("register")

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "สมัครสมาชิกสําเร็จ")
        storage = messages.get_messages(request)
        storage.used = True
        return redirect("register")
    else:
        return render(request, "register.html")


def login(request: WSGIRequest):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if not username or not password:
            messages.warning(request, "กรุณาป้อนข้อมูลให้ครบถ้วน")
            return redirect("login")

        user = authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "เข้าสู่ระบบสําเร็จ")
            storage = messages.get_messages(request)
            storage.used = True
            return redirect("index")
        else:
            messages.warning(request, "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
            return redirect("login")
    else:
        return render(request, "login.html")


def logout(request):
    auth.logout(request)
    return redirect("login")
