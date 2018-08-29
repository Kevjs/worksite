from django.shortcuts import render, redirect, reverse, HttpResponse
from django.http import JsonResponse
from .models import Message, Thread
from ..LandR.models import User, Title

# Create your views here.
def home(request):
    a = { "level" : User.objects.get(sessionId=request.session["sId"]).website_power.level }
    return render(request, "user/index.html", a)

def messages(request):
    data = {
        "titles":Title.objects.all()
    }
    return render(request, "user/messages.html", data)

def allmessages(request, latest=False):
    temp = Thread.objects.filter(users__in=User.objects.filter(sessionId=request.session["sId"]))
    new = User.objects.get(sessionId = request.session["sId"]).new_threads.all()
    temp = temp.order_by("-updated_at")
    if latest:
        temp = temp[:5]
    return render(request, "user/allmessages.html", {"threads":temp, "new":new})

def readThread(request, id):
    target = Thread.objects.get(id=id)
    target.newFor.remove(User.objects.get(sessionId = request.session["sId"]))
    return HttpResponse("read it")

def userOnTables(request):
    search = User.objects.exclude(sessionId=request.session["sId"])
    search = search.filter(first_name__startswith=request.POST["name"])
    titles = Title.objects.all()
    for title in titles:
        if title.title not in request.POST:
            search = search.exclude(title=Title.objects.get(title=title.title))
    if(request.POST["many"] == "all"):
        return render(request, "user/tables.html", {"users":search})
    start = (int(request.POST["page_number"]) - 1) * int(request.POST["many"])
    end = start + int(request.POST["many"])
    if (end - start) > len(search):
        return render(request, "user/tables.html", {"users":search})
    pages = "a"*(((len(search)-1)//int(request.POST["many"]))+1)
    search = search[start:end]
    return render(request, "user/tables.html", {"users":search, "pages":pages})

def newMessage(request):
    a = Message.objects.creator(postData = request.POST, sId = request.session["sId"])
    if "success" in a:
        return HttpResponse("Success")
    return JsonResponse({"hi":a})
# def dec(request, id = None)