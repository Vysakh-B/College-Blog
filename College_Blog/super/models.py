from django.db import models
from register.models import Profile
from posts.models import post


# Create your models here.
class Magazine(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('register.Profile', on_delete=models.CASCADE)
    post_id = models.ForeignKey('posts.post', on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Magazine {self.id} - User {self.user_id} - Post {self.post_id}"