from django.urls import path, include
from . import views

app_name = 'auth'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.signin, name='login'),
    path('register/', views.register, name='register'),
    path('register/varify_email/<str:name>/<str:EMAIL>/<str:password>/',
         views.varify_email, name='reg_email'),
    path('logout/', views.signout, name='logout'),
    path('forgot_password/', views.forgot_password,  name="fpass"),
    path('forgot_password/<str:email>/', views.reset_password,  name="rpass"),
    path('new_password/<str:email>/', views.create_a_new_passwword,  name="cpass"),
]
