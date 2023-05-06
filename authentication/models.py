from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import MyUserManager
# Create your models here.

class MyAbstractBaseUser(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=255, primary_key=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        abstract = True

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

class CustomUser(MyAbstractBaseUser, PermissionsMixin):
    middle_name= models.CharField(max_length=200, blank=True, null=True)
    phone= models.CharField(max_length=10, blank=True, null=True)
    address= models.CharField(max_length=256, blank=True, null=True)
    profile_image= models.ImageField(default="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS274bc75lVP83oHXqnPlMrx3fH3ZsUr2T7MQ&usqp=CAU", blank=True)

    def __str__(self):
        return str(self.email)