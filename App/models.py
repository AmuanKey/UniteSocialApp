from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
# Create your models here.

class CategoryModel(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class PostModel(models.Model):
    title= models.CharField(max_length=100)
    body = models.TextField()
    image = models.ImageField(blank=True, default=None)
    created_at = models.DateTimeField(default=datetime.now)
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE,blank=True , null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.title

class CommentModel(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.content




