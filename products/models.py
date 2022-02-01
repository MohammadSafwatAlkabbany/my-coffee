from django.db import models
from datetime import datetime

from django.db.models.fields import TextField
# Create your models here.
class Product(models.Model):
    name= models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_active = models.BooleanField(default=True)
    photo = models.ImageField(upload_to = 'photo/%y/%m/%d/')
    publish_date = models.DateTimeField(default=datetime.now)


    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-publish_date']