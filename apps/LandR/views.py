from django.shortcuts import render, redirect, reverse, HttpResponse
from .models import User

# Create your views here.
def home(request):
    any = User.objects.all()
    if any:
        return render(request, "LandR/index.html")
    return redirect(reverse("login:first"))

def login(request):
    status = User.objects.logger(request.POST)
    if "success" in status:
        request.session["sId"] = status["success"].sessionId
        request.session["name"] = "{} {}".format(status["success"].first_name, status["success"].last_name)
        return HttpResponse("Success")
    return HttpResponse("Fail")

def logout(request):
    request.session.clear()
    return redirect("login:home")

def first(request):
    any = User.objects.all()
    if any:
        return redirect(reverse("login:home"))
    return render(request, "LandR/first.html")

def firstP(request):
    any = User.objects.all()
    if not any:
        status = User.objects.first(request.POST)
        if "success" in status:
            request.session["sId"] = status["success"].sessionId
            request.session["name"] = "{} {}".format(status["success"].first_name, status["success"].last_name)
            return HttpResponse("Success")
    return HttpResponse("Fail")