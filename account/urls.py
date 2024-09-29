from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.loginpage, name='login'),
   # path('logout/', LogoutView.as_view(), name='logout'),
    path('room/',views.show_frend,name='friend'),
    path('send_friend_request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('accept_friend_request/<int:user_id>/', views.accept_friend_request, name='accept_friend_request'),
]
