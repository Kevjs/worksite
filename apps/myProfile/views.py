from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from ..LandR.models import User

# Create your views here.
def home(request):
    return render(request, "myProfile/index.html", {"me":User.objects.get(sessionId = request.session["sId"])})