from django.db import models
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
    def __str__(self):
        return str(self.user)
