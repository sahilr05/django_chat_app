import uuid, typing
from accounts.types import UserGenderType, UserState, states_as_list
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    user.status = UserState.ONLINE
    user.save()

@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    user.status = UserState.OFFLINE
    user.save()


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)



class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_picture_url = models.URLField(max_length=2048, blank=True)
    username = models.CharField(max_length=40, unique=False, default='')
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50, blank=True)
    status = models.CharField(choices=states_as_list(UserState), max_length=20)
    gender = models.CharField(choices=states_as_list(UserGenderType), max_length=20)
    country = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^(\+\d{1,3})?,?\s?\d{8,13}', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
    interests = models.ManyToManyField('Interest')

    USERNAME_FIELD = "email"
    objects = UserManager()

    REQUIRED_FIELDS: typing.List[str] = []

    def clean(self):
        super().clean()
        if not self.email and not self.phone_number:
            raise ValidationError("At least one of email or phone number must be provided.")

class Interest(models.Model):
    interest_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
