from django.db import models
from django.utils import timezone
# from django.contrib.auth import get_user_model
# from register.models import User
# Create your models here.
class post(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('register.Profile', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    blog_picture = models.ImageField(upload_to='blog_pictures/')
    created_at = models.DateTimeField(auto_now_add=True)
    like = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    admin_comment = models.TextField(blank=True, null=True)
    showing = models.BooleanField(default=True)
    def __str__(self):
        return str(self.user)


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    post_id = models.ForeignKey('post', on_delete=models.CASCADE)  # ForeignKey to Post model
    user_id = models.ForeignKey('register.Profile', on_delete=models.CASCADE)  # ForeignKey to User model
    comment_description = models.TextField()  # Field for the comment description
    report_count = models.IntegerField(default=0)  # Integer field for report count, default is 0
    commented_at = models.DateTimeField(default=timezone.now)  # DateTime field for the comment date and time

    def __str__(self):
        return f"Comment by {self.user_id} on {self.post_id}"
class Bookmark(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.ForeignKey('register.Profile', on_delete=models.CASCADE, related_name="bookmarks")
    postid = models.ForeignKey('Post', on_delete=models.CASCADE, related_name="bookmarked_by")

    class Meta:
        unique_together = ('userid', 'postid')  # Ensures a user can't bookmark the same post multiple times
        ordering = ['id']  # Optional: orders bookmarks by their creation id

    def __str__(self):
        return f"Bookmark by {self.userid} on {self.postid}"
class Likes(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('register.Profile', on_delete=models.CASCADE, related_name="liked_by")
    post_id = models.ForeignKey('Post', on_delete=models.CASCADE, related_name="liked")
    liked_at = models.DateTimeField(default=timezone.now)  # DateTime field for the comment date and time

    class Meta:
        unique_together = ('user_id', 'post_id')  # Ensures a user can't bookmark the same post multiple times
        

    def __str__(self):
        return f"Liked by {self.user_id} on {self.post_id}"