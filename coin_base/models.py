from django.db import models
from authentication.models import CustomUser
import hashlib
import uuid

# Create your models here.

class Coin(models.Model):
    coin_id= models.UUIDField(primary_key=True, default=uuid.uuid4)
    owner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Generate hash using user's username and current timestamp
        string_to_hash = f"{self.owner.email}-{self.created_at.timestamp()}"
        hash_object = hashlib.sha256(string_to_hash.encode())
        hash_hex = hash_object.hexdigest()

        # Save the hash to the model instance
        self.hash = hash_hex

        super().save(*args, **kwargs)

class CoinUserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, null=True)
    coins = models.ForeignKey(Coin, related_name='coins_owner', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.first_name
    
class Transaction(models.Model):
    sender = models.ForeignKey(CoinUserProfile, on_delete=models.SET_NULL,null=True, related_name='sender')
    receiver = models.ForeignKey(CoinUserProfile, on_delete=models.SET_NULL,null=True, related_name='receiver')
    coins = models.ForeignKey(Coin, on_delete=models.SET_NULL,null=True, related_name='coin_transfer')

    def __str__(self):
        return f"{self.sender} sent {self.coins} coins to {self.receiver}"
