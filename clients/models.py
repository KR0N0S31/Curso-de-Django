from django.db import models
# from products.models import Product
# Create your models here.

class Client(models.Model):
    name = models.CharField(max_length=255)
    phone = models.IntegerField(unique=True)
    email = models.EmailField(max_length=255,unique=True)
    address = models.CharField(max_length=255)
    # productos = models.ManyToManyField(Productos)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)
