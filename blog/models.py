from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.

class UserMedia(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    class Meta:
        verbose_name_plural = "User Media"

    def __str__(self):
        return self.user.username



class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    text = models.TextField()
    draft = models.BooleanField(default=False, null=False)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Posts"

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title



class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    replyto_id = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    replyto_text = models.TextField(blank=True, null=True)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Comments"

    def __str__(self):
        return f"Comment to: {self.post.title}/By: {self.author}/Date: {self.created_date}"
    