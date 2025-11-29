from time import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin 
import bcrypt
# from apps.permissions.models import Role

def hash_password(raw_password):
    salt = bcrypt.gensalt(rounds=12) 
    return bcrypt.hashpw(raw_password.encode("utf-8"), salt).decode("utf-8")

def check_password(raw_password, hashed):
    return bcrypt.checkpw(raw_password.encode("utf-8"), hashed.encode("utf-8"))

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique = True)
    first_name = models.CharField(max_length = 100, blank = True)
    last_name = models.CharField(max_length = 100, blank = True)
    middle_name = models.CharField(max_length = 100, blank = True, null = True)
    
    is_active = models.BooleanField(default = True)
    is_superuser = models.BooleanField(default = False)
    
    date_joined = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    deleted_at = models.DateTimeField(null = True, blank = True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_role_names(self):
        if self.pk:
            return list(
                self.user_roles.filter(is_active=True)
                .values_list("role__name", flat=True)
            )
        return []
    
    def set_password(self, raw_password):
        if raw_password is not None:
            self.password = hash_password(raw_password)

    def check_password(self, raw_password):
        if self.password is None or self.password == "":
            return False
        return check_password(raw_password, self.password)

    def soft_delete(self):
        self.is_active = False
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_active", "deleted_at"])
        
    def __str__(self):
        return self.email
    