from django.urls import reverse

from django.db import models
from django.contrib.auth.models import AbstractUser
from taggit.managers import TaggableManager


class User(AbstractUser):
    # Custom user model
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="تاریخ تولد")
    bio = models.TextField(max_length=120, null=True, blank=True, verbose_name="بایو")
    photo = models.ImageField(upload_to="account_images/", null=True, blank=True, verbose_name="تصویر")
    job = models.CharField(max_length=120, null=True, blank=True, verbose_name="شغل")
    phone = models.CharField(max_length=11, verbose_name="موبایل")


class Post(models.Model):
    # User posts model
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author', verbose_name='نویسنده')
    description = models.TextField(verbose_name='متن')
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    tags = TaggableManager()

    class Meta:
        ordering = ['-create']
        indexes = [
            models.Index(fields=['-create']),
        ]
        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'

    def __str__(self):
        return self.author.first_name

    def get_absolute_url(self):
        return reverse('social:post_detail', args={self.id})
