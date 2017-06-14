from django.db import models


class ig_img(models.Model):
    username = models.CharField(blank=True,max_length=100)
    url = models.URLField(blank=True)
    CreateDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id

# Create your models here.
class img(models.Model):
    title = models.CharField(blank=True,max_length=100)
    photo = models.URLField(blank=True)
    CreateDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id
