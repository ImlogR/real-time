# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth import get_user_model
# from .models import Wallet

# User = get_user_model()

# @receiver(post_save, sender=User)
# def create_wallet(sender, instance, created, **kwargs):
#     if created:
#         Wallet.objects.create(owner=instance)

# @receiver(post_save, sender=User)
# def save_wallet(sender, instance, **kwargs):
#     instance.wallet.save()