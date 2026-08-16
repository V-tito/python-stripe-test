from django.db import models

class Item(models.Model):
    id=models.IntegerField(primary_key=True)
    name=models.CharField()
    description=models.TextField()
    price=models.FloatField()
    currency=models.CharField(max_length=3)

class Discount(models.Model):
    id=models.IntegerField(primary_key=True)
class Tax(models.Model):
    id=models.IntegerField(primary_key=True)
# Create your models here.
class Order(models.Model):
    id=models.IntegerField(primary_key=True)
    items=models.ManyToManyField(Item)
    discount=models.ForeignKey(Discount,on_delete=models.SET_NULL,null=True,blank=True)
    tax=models.ForeignKey(Tax,on_delete=models.SET_NULL,null=True,blank=True)
    def __str__(self):
        return f"Order {self.id}"

