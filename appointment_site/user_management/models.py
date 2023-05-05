from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser, UserManager, PermissionsMixin
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# User = get_user_model()

class UserManagers(UserManager):
    use_in_migrations = True

    def _create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("The given email must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            self.validate_password(password)
            user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self._create_user(email, password, **extra_fields)

    def validate_password(self, password):
        if len(password) < 8:
            raise ValidationError(_('Password must be at least 8 characters long.'))

class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    user_permissions = None
    groups = None
    last_login = None
    date_joined = None
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255,null=True,blank=True)
    objects = UserManagers()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    # def __str__(self):
    #     return self.name


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    


class Counsellor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    
    

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE,null=True)
    counsellor = models.ForeignKey(Counsellor, on_delete=models.CASCADE,null=True)
    appointment_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    # def __str__(self):
    #     return self.appointment_date.strftime("%m/%d/%Y, %H:%M:%S")

