from django.urls import path
from . import views

urlpatterns = [
    path('single/<int:id>/',views.single,name='single'),
    path('feed',views.feed,name='feed'),
    path('create',views.create,name='create'),
    path('search',views.search,name='search'),   
    path('edit',views.edit,name='edit'),
    path('addcomment/<int:post_id>/',views.addcomment,name='addcomment'),

]