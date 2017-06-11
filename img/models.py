from django.db import models

# Create your models here.
class img(models.Model):
    title = models.CharField(blank=True,max_length=100)
    photo = models.URLField(blank=True)
    CreateDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title