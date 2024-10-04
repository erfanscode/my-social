from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # Custom user model
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="تاریخ تولد")
    bio = models.TextField(max_length=120, null=True, blank=True, verbose_name="بایو")
    photo = models.ImageField(upload_to="account_images/", null=True, blank=True, verbose_name="تصویر")
    job = models.CharField(max_length=120, null=True, blank=True, verbose_name="شغل")
    phone = models.CharField(max_length=11, verbose_name="موبایل")
