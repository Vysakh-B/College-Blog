from django.contrib import admin

from .models import post,Comment,Bookmark,Likes

admin.site.register(post)
admin.site.register(Comment)
admin.site.register(Bookmark)
admin.site.register(Likes)


