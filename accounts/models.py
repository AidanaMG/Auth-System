from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from .auth import hash_password


class UserManager(BaseUserManager):
   

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.password = hash_password(password) 
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    last_name = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)

    role = models.ForeignKey(
        "permissions.Role",
        on_delete=models.PROTECT,
        related_name="users",
        null=True,
    )

    is_active = models.BooleanField(default=True) 
    is_staff = models.BooleanField(default=False)  
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"  
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
class BlacklistedToken(models.Model):
    token = models.TextField(unique=True)
    blacklisted_at = models.DateTimeField(auto_now_add=True)