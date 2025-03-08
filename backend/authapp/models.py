from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.db import models

from BookingApplication.constants import LANGUAGES



class User(AbstractUser):
    email = models.EmailField(verbose_name="email",
                              max_length=254, unique=True)
    username = models.CharField(max_length=127,unique=True)
    first_name =models.CharField(max_length=127,null=True,blank=True)
    last_name =models.CharField(max_length=127,null=True,blank=True)
    terms_cond = models.BooleanField(default=False)
    # TODO update me , when implement activate user via email
    is_active = models.BooleanField(default=False)

    REQUIRED_FIELDS = ["terms_cond"]
    def __str__(self):
        return self.username


class Profile(models.Model):
    username = models.CharField(max_length=127)
    email = models.EmailField(verbose_name="email",unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=127, blank=True, null=True)
    last_name = models.CharField(max_length=127, blank=True, null=True)
    # NOTE: we can use a package from pip to have acces to all countries and cities !
    age = models.PositiveIntegerField(
        blank=True,
        null=True,
        validators=[
            MinValueValidator(1, message='Age is no allowed')]
    )
    location = models.CharField(max_length=100, blank=True, null=True)
    languages = models.CharField(
        max_length=20, choices=LANGUAGES.choices, default=LANGUAGES.ARABIC)

    def save(self, *args, **kwargs):
        if self.username and self.user.username != self.username:
            self.user.username = self.username
            self.user.save()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.user.username}"
