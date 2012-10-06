from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=60)
    def __unicode__(self):
        return self.name

class Tags(models.Model):
    name = models.CharField(max_length=60)
    def __unicode__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=120)
    author = models.ForeignKey(User)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField()
    body = models.TextField()
    published = models.DateTimeField(default=datetime.now)
    categories = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tags)
    image = models.ImageField(upload_to='images/')

    def __unicode__(self):
        return self.title
    class Meta:
        ordering = ['-published']
    def get_absolute_url(self):
        return "/%s/%s/%s/" % (self.published.year, self.published.month, self.slug)

