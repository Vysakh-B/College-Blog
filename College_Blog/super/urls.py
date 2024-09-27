from django.urls import path
from . import views

urlpatterns = [
    path('super',views.superu,name="super"),
    path('adminhome',views.adminhome,name = "adminhome"),

    # path('signin',views.signin,name='signin'),
    #path('logout',views.logout,name='logout'),
]
