from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('signin',views.signin,name='signin'),
    path('about',views.about,name='about'),
    path('contact',views.ctct,name='contact'),
    path('home',views.home,name='home'),
    path('profile',views.account,name='profile'),
    path('register',views.register,name='register'),
    # path('signin',views.signin,name='signin'),
    path('logout',views.logout,name='logout'),
]
