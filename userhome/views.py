from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Film, user_history
# Create your views here.

@login_required(login_url='/login/')
def index(request):
    a = Film.objects.all()
    history = get_object_or_404(user_history, user=request.user)
    newlist = []
    history_list = history.get_history
    return render(request, 'ush/video.html', {'films':a,'history':history_list})

@login_required(login_url='/login/')
def video_page_function(request, title):    
    video =  get_object_or_404(Film, title=title)
    film_order_list = get_object_or_404(user_history, user=request.user) 
    film_order_list.append_history(video.title.replace(" ", "_"))
    film_order_list.save()
    return render(request, "ush/videopage.html",{'video':video})

