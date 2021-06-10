from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager

class User(AbstractBaseUser):
    
    email = models.EmailField(max_length=100, unique=True, verbose_name="email address")
    name = models.CharField(max_length=50)
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = UserManager()

    def __str__(self):
        return self.email
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True
        
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin