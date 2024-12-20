from django.urls import path
from . import views

urlpatterns = [
    path('single/<int:id>/',views.single,name='single'),
    path('feed',views.feed,name='feed'),
    path('create',views.create,name='create'),
    path('search',views.search,name='search'),   
    path('edit',views.edit,name='edit'),
    path('addcomment/<int:post_id>/',views.addcomment,name='addcomment'),
    path('editpost/<int:post_id>/',views.editpost,name='editpost'),
    path('singleview/<int:profile_id>',views.singleview,name='singleview'),
    path('removepost/<int:post_id>/',views.removepost,name='removepost'),
    path('addreport/<int:c_id>/<int:p_id>/',views.addreport,name='addreport'),
    path('bookmark/<int:id>/',views.bookmark,name='bookmark'),
    path('booked',views.booked,name='booked'),
    path('singleprofile/<int:id>/',views.singleprofile,name='singleprofile'),
    path('toggle-like/<int:id>/', views.toggle_like, name='toggle_like'),
    

    

]