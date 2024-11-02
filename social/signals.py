from django.db.models.signals import m2m_changed, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Post


@receiver(m2m_changed, sender=Post.likes.through)
def users_like_change(sender, instance, **kwargs):
    instance.total_likes = instance.likes.count()
    instance.save()

@receiver(post_delete, sender=Post)
def post_delete_send_email(sender, instance, **kwargs):
    author = instance.author
    subject = "پست شما حذف شد"
    message = f"پست شما با آیدی {instance.id} حذف شد."
    send_mail(subject, message, settings.EMAIL_HOST_USER, [author.email], fail_silently=False)