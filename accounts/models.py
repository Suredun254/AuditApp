from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from .managers import UsersManager
from django.utils import timezone

# Create your models here.
        
class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(default='N/A', max_length=50)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UsersManager()
    
    USERNAME_FIELD ='email'
    REQUIRED_FIELDS = []

    # Add related_name for groups and user_permissions
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='user_accounts',
        related_query_name='user_account'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='user_accounts',
        related_query_name='user_account'
    )

    def __str__(self):
        return self.email