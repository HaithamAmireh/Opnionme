from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import WatchList, Item
from .forms import CreateNewList
# Create your views here.

def index(response, id):
    ls = WatchList.objects.get(id = id)
    if ls in response.user.watchlist.all():

        #{"save":["save"], "c1":["clicked"]}
        if response.method == 'POST':
            print(response.POST)
            if response.POST.get("save"):
                for item in ls.item_set.all():
                    if response.POST.get("c" + str(item.id)) == "clicked":
                        item.complete = True
                    else:
                        item.complete = False
                    item.save()
            elif response.POST.get("newItem"):
                txt = response.POST.get("new")
                desc = response.POST.get("details")
                if len(txt) > 2 and len(desc) > 1:
                    ls.item_set.create(text = txt, description = desc ,complete = False)
                else:
                    print("invalid input")
        return render(response,"main/list.html",{"ls":ls})
    return render(response,"main/view.html",{})

def home(response):
    return render(response,"main/home.html",{})

def create(response):
    if response.method == "POST":
        form = CreateNewList(response.POST)
        if form.is_valid():
            n = form.cleaned_data["name"]
            w = WatchList(name = n)
            w.save()
            response.user.watchlist.add(w)

        return HttpResponseRedirect("/%i"%w.id)
    else:
        form = CreateNewList()
    return render(response,"main/create.html",{"form":form})

def view(response):
    return render(response, "main/view.html",{})