from django.db import models
from datetime import datetime
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User



class Department(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    department = models.ForeignKey(Department, on_delete=CASCADE)
    brand = models.CharField(max_length=200, blank=True)
    name = models.CharField(max_length=200, unique=True)
    price = models.IntegerField(null=False)
    dozen_price = models.IntegerField(blank=True, null=True)
    quantity = models.IntegerField(default=0)
    time_added = models.DateTimeField(default=datetime.now, blank=True)
    updated = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-quantity', '-price']
    
    def __str__(self):
        return self.name


class Batch(models.Model):
    item = models.ForeignKey(Item, on_delete=CASCADE)
    batch_rank = models.IntegerField(default=0)
    batch_date = models.DateTimeField(default=datetime.now, blank=True)
    batch_expiry_date = models.DateTimeField(null=True, blank=True)
    item_purchased = models.IntegerField(default=0)
    
    def __repr__(self):
        return self.batch_rank

    class Meta:
        verbose_name_plural = 'Batches'


class Sale(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    price = models.IntegerField(blank=True)
    quantity = models.IntegerField(blank=True)
    time_sold = models.DateTimeField(auto_now=True)
    

    class Meta:
        ordering = ['-time_sold']
    
    def __str__(self):
        return str(self.quantity)


class Cart(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=2)
    price = models.IntegerField(blank=True)
    quantity = models.IntegerField(blank=True)
    time_added = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-quantity', '-price']
    
    def __str__(self):
        return str(self.id)


