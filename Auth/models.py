from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
# Create your models here.

class User(AbstractUser):
    ROLES = [
        ('user','User'),
        ('seller','Seller')
    ]
    id = models.UUIDField(default=uuid.uuid4,primary_key=True)
    email = models.EmailField(unique=True,null=False)
    username = models.CharField(unique=True,null=False,max_length=100)
    mobile = models.CharField(max_length=15)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.CharField(choices=ROLES,default='user',max_length=100)
    
    USERNAME_FIELD ='email'
    REQUIRED_FIELDS = ['username',]
    
    def fullname(self):
        return f"{super().first_name} {super().last_name}"
    
    def __str__(self):
        return self.email
    