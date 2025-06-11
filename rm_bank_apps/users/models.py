import re
from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager
from django.core.exceptions import ValidationError

def validate_cnic(value):
    pattern = r'^\d{5}-\d{7}-\d{1}$'
    if not re.match(pattern, value):
        raise ValidationError("CNIC must be in the format 12345-1234567-1")

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    email = models.EmailField(unique=True)
    CNIC = models.CharField(max_length=15, unique=True, validators=[validate_cnic])
    DOB = models.DateField()
    address = models.TextField()
    roles = models.ManyToManyField(Role)
    created_at = models.DateTimeField(auto_now_add=True)
    
    objects = CustomUserManager()
    