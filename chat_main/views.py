from django.shortcuts import render
from .import views

# Create your views here.
def show(request):
    return render (request,'room/html.html')


def room(request, room_name):
    return render(request, 'room/html.html', {"room_name": room_name})    