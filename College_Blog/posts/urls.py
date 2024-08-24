from django.urls import path
from . import views

urlpatterns = [
    path('magazine',views.magazine,name='magazine'),
    path('single',views.single,name='single'),
    path('feed',views.feed,name='feed'),
    path('create',views.create,name='create'),
    path('search',views.search,name='search'),   
    path('edit',views.edit,name='edit'),
]