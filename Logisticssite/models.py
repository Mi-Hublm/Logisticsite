from django.db import models


# Create your models here.

class Post(models.Model):
    # author = models.ForeignKey(on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField
    decs = models.CharField(max_length=500, default="This is a default description.")
    body = models.TextField()
    image = models.FileField(upload_to='blog-post-image')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Team(models.Model):
    name = models.CharField(max_length=200)
    image = models.FileField(upload_to='team-img')
    position = models.CharField(max_length=100)

    def __str__(self):
        return self.name