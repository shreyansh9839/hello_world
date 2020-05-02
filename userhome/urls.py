from django.urls import path, include
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.index, name='index'),
    path('video_player/<str:title>', views.video_page_function, name='video_page'),
]


