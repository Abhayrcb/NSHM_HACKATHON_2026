from django.db import models
import uuid
from Auth.models import User
# Create your models here.
class Product(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    name = models.CharField(max_length=100,null=False)
    description = models.TextField()
    image = models.URLField(null=True,blank=True)
    price = models.FloatField()
    
    created_at = models.DateField(auto_now_add=True,blank=True,null=True)
    def sku(self):
        return f"{self.name}-{self.id}"
    def __str__(self):
        return self.name

class Inventory(models.Model):
    seller = models.ForeignKey(User,on_delete=models.CASCADE,related_name='inventory_seller')
    product = models.OneToOneField(Product,on_delete=models.CASCADE,related_name='inventory')
    stock = models.IntegerField()
    reorder_level = models.IntegerField()
    
    def __str__(self):
        return f"Inventory for {self.product.name} - Stock: {self.stock}"
        

class Sale(models.Model):
    id = models.UUIDField(default=uuid.uuid4,primary_key=True)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    sale_date = models.DateField(auto_now_add=True)
    quantity_sold = models.IntegerField()
    
    
    def __str__(self):
        return f"Sale of  on {self.sale_date} - Quantity: {self.quantity_sold}"
