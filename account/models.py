from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin



# Create your models here.
class MyAccountManager( BaseUserManager ):

    def create_user(self, email,username, password=None, is_staff=False, is_superuser=False ):
        if not email:
            raise ValueError("User must have an email address")
        if not username:
            raise ValueError("User must have an username")
        user = self.model( email = email, username = username )
        user.is_staff = is_staff
        # user.is_admin = is_admin
        user.is_superuser = is_superuser
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,email, username, password=None):
        user = self.create_user( email,username,password, True , True )
        return user



class Account( AbstractBaseUser,PermissionsMixin):
    email    = models.EmailField(max_length=45, unique=True)
    username = models.CharField(max_length=45, unique = True) 
    date_join = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    date_login = models.DateTimeField(verbose_name='last login', auto_now_add=True)
    is_admin = models.BooleanField(default = False)
    is_active = models.BooleanField( default= True)
    is_staff = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = MyAccountManager()

    def __str__(self):
        return self.email
    def has_perm(self, perm, boj = None):
        return self.is_superuser

    def has_module_perm(self, app_level):
        if self.is_superuser:
            return True
        return False
    def has_module_perms(self, perms, obj=None):
	    return all(self.has_perm(perm, obj) for perm in perms)        
    