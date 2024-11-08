from django.urls import path
from . import views

urlpatterns = [
    path('super',views.superu,name="super"),
    path('adminhome',views.adminhome,name = "adminhome"),
    path('singlemagazine/<int:id>/',views.singlemagazine,name = "singlemagazine"),
    path('pending',views.pending,name = "pending"),
    path('reject/<int:post_id>/',views.reject,name = "reject"),
    path('accept/<int:id>/',views.accept,name="accept"),
    path('magazine/<int:id>/',views.magazine,name="magazines"),
    path('acceptuser/<int:id>/',views.acceptuser,name="acceptuser"),
    path('removecomment/<int:id>/',views.removecomment,name="removecomment"),
    path('user_pending',views.userpending,name="userpending"),
    path('viewmagazine',views.viewmagazine,name='magazine'),
    path('reports',views.reports,name='reports'),

    
    # path('signin',views.signin,name='signin'),
    #path('logout',views.logout,name='logout'),
]
