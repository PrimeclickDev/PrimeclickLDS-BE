import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator, EmailValidator


email_validator = EmailValidator()

phone_regex = RegexValidator(
    regex=r"^\d{10}", message="Phone number must be 13 digits only!"
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(
                "Email field must be set.")

        # Normalize the email and phone number
        email = self.normalize_email(email) if email else None
        # phone_number = self.normalize_phone_number(
        #     phone_number) if phone_number else None

        # Create the user instance
        user = self.model(
            email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email=email, password=password, **extra_fields)

    def normalize_phone_number(self, phone_number):
        """
        Normalize the phone number by removing non-digit characters.
        """
        return ''.join(filter(str.isdigit, str(phone_number)))


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(
        max_length=255, unique=True, validators=[email_validator])
    phone_number = models.CharField(
        max_length=30, unique=True, blank=True, null=True, validators=[phone_regex])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        return self.first_name

    def __str__(self):
        return self.first_name
