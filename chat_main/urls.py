from django.urls import path ,include
from .import views
urlpatterns = [
    path('room/',views.show,name='room'),
    path('/<str:room_name>/', views.room, name="room"),

]