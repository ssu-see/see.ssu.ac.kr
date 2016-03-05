from django.shortcuts import render, redirect
from boards.views import Board


def home(request):
    boardlist = Board.objects.all()
    return render(request, "home.html", {'boardlist': boardlist})


def aboutus(request):
    return redirect('home')
