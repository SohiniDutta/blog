from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.

class postModel(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    title  = models.CharField(max_length=255)
    text   = models.TextField()
    created_date = models.DateTimeField(default=timezone.now())
    publish_date = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return self.title

    def publish(self):
        self.publish_date = timezone.now()
        self.save()

    def approved_comments(self):
        return self.comments.filter(approved_stat=True)

    def get_absolute_url(self):
        return reverse('blog_app:post-detail',kwargs={'pk':self.pk})

    
class commentModel(models.Model):
    post   = models.ForeignKey(postModel,related_name='comments',on_delete=models.CASCADE)
    author = models.CharField(max_length=255)
    text   = models.TextField()
    created_date  = models.DateTimeField(default=timezone.now)
    approved_stat = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    def approve(self):
        self.approved_stat = True
        self.save() 

    def get_absolute_url(self):
        return reverse('blog_app:post-list')
