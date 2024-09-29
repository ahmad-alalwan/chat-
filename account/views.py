from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from.models import*
# Create your views here.
def accept_request(request):
    if request.method == "POST":
        username = request.POST.get("username")
        user = request.user
        friend = User.objects.get(username=username)
        accepted = True

        exists = UserRelation.objects.filter(user=user, friend=friend).exists()
        print("sts")
        if exists:
            return HttpResponseRedirect(
                request.META.get("HTTP_REFERER", reverse("home"))
            )
        user_relation = UserRelation(user=user, friend=friend, accepted=accepted)
        user_relation.save()

        user_relation_revrse = UserRelation.objects.get(user=friend, friend=user)
        user_relation_revrse.accepted = True
        user_relation_revrse.save()
        messages.success(request, "Friend Added successfully.")

        return redirect("home")
    else:
        return redirect("home")
def add_friend(request):
    if request.method == "POST":
        username = request.POST.get("username")
        user = request.user
        friend = User.objects.get(username=username)
        accepted = False
        print("starts")
        exists = UserRelation.objects.filter(user=user, friend=friend).exists()
        print("sts")
        if exists:
            print("star")
            return HttpResponseRedirect(
                request.META.get("HTTP_REFERER", reverse("home"))
            )
        user_relation = UserRelation(user=user, friend=friend, accepted=accepted)
        user_relation.save()
        messages.success(request, "Request sended successfully.")

        return redirect("home")
    else:
        return redirect("home")        

def search(request):
    if request.method == "GET":
        query = request.GET.get("q", "")
        if query:
            users = User.objects.filter(username__icontains=query)
            if users:
                return render(
                    request,
                    "search.html",
                    {"query": query, "users": users, "user": request.user.username},
                )
            else:
                not_found_message = f'No users found for "{query}"'
                return render(
                    request,
                    "search.html",
                    {
                        "query": query,
                        "not_found_message": not_found_message,
                    },
                )

    return render(request, "search.html", {"user": request.user.username})        

def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return render(request,'room/html.html')  
            else:
                return render(request, 'login/login.html', {'error': 'Invalid credentials'})
        else:
            return render(request, 'login/login.html', {'error': 'Please provide both username and password'})
    return render(request, 'login/login.html')
def show_frend(request):
    user = request.user
    friends = UserRelation.objects.filter(models.Q(user=user) | models.Q(friend=user),accepted=True )
    return render(request, 'room/html.html', {'friends': friends})
def accept_friend_request(request, user_id):
    relation = get_object_or_404(UserRelation, user__id=user_id, friend=request.user)
    relation.accepted = True
    relation.save()
    return redirect('friend')  # Redirect to the friends page
def send_friend_request(request, user_id):
    friend = get_object_or_404(User, id=user_id)
    if request.user != friend:  # Prevent sending a friend request to oneself
        UserRelation.objects.get_or_create(user=request.user, friend=friend)
    return redirect('friend')  # Redirect to the friends page
     

