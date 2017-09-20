from django.db import models
from clients.models import Client
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(blank = True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name

class Favorite(models.Model):
    user = models.ForeignKey(Client)
    product = models.ForeignKey(Product)

    class Meta:
        verbose_name = 'Favorite'
        verbose_name_plural = 'Favorites'

    def __str__(self):
        return '%s %s' %(self.user, self.product)
