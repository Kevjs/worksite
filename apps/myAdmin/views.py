from django.shortcuts import render, HttpResponse, redirect, reverse
from ..LandR.models import User, Title, Level
from django.http import JsonResponse
# Create your views here.
def home(request):
    if "sId" not in request.session:
        request.session.clear()
        return redirect(reverse("login:logout"))
    if User.objects.get(sessionId=request.session["sId"]).website_power.level < 500:
        return redirect(reverse("main:home"))
    data = {
        "titles": Title.objects.all(),
        "levels": Level.objects.all(),
    }
    return render(request, "myAdmin/index.html", data)

def newUser(request):
    if "sId" not in request.session:
        request.session.clear()
        return redirect(reverse("login:logout"))
    if User.objects.get(sessionId=request.session["sId"]).website_power.level < 500:
        return redirect(reverse("main:home"))
    status = User.objects.creator(sId = request.session["sId"], postData = request.POST)
    if "success" in status:
        return HttpResponse("Success")
    return JsonResponse(status)