from django.db import models



class LANGUAGES(models.TextChoices):
    ARABIC = 'AR', 'Arabic'
    ENGLISH = 'EN', 'English'
    FRENCH = 'FR', 'French'
    SPANISH = 'ES', 'Spanish'
    # and other languages

    # we used for define default value coz it should be callable for ArrayField
    @staticmethod
    def default_language():
        return [LANGUAGES.ENGLISH]


class PROPERTY_STATUS_CHOICES(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    CANCELED = 'CANCELED', 'Canceled'
    CONFIRMED = 'CONFIRMED', "Confirmed"
