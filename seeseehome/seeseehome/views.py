from django.shortcuts import render
from boards.views import Board


def home(request):
    boardlist = Board.objects.all()
    return render(request, "home.html", {'boardlist': boardlist})


def aboutus(request):
    boardlist = Board.objects.all()
    return render(request, "aboutus.html", {'boardlist': boardlist})
