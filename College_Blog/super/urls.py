from django.urls import path
from . import views

urlpatterns = [
    path('super',views.superu,name="super"),
    path('adminhome',views.adminhome,name = "adminhome"),
    path('pending',views.pending,name = "pending"),
    path('reject/<int:post_id>/',views.reject,name = "reject"),
    path('accept/<int:id>/',views.accept,name="accept"),
    path('acceptuser/<int:id>/',views.acceptuser,name="acceptuser"),
    path('user_pending',views.userpending,name="userpending"),

    # path('signin',views.signin,name='signin'),
    #path('logout',views.logout,name='logout'),
]
