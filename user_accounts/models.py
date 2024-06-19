from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, contactNumber, password=None, **extra_fields):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            username=username,
            contactNumber=contactNumber,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, contactNumber, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username,
            password=password,
            contactNumber=contactNumber,
        )

        user.set_password(password)

        user.is_staff = True
        user.active = True
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user

  

# this is a custom user model.
class CustomUser(AbstractUser):
    email = models.EmailField(max_length=200, blank=False, unique=True, null=True)
    saleads_id = models.CharField(max_length=20, unique=True, blank=False, null=True)
    contactNumber = models.CharField(max_length=20, blank=True, null=True)
    terms = models.BooleanField(blank=False, null=True)

    objects = CustomUserManager()

    # USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['contactNumber']

    class Meta:
        ordering = ['first_name']
        verbose_name_plural = ('Users')

    def __str__(self):
        return self.username













