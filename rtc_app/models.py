from django.db import models
import uuid
from authentication.models import CustomUser
import hashlib
# Create your models here.
class GroupModel(models.Model):
    group_id= models.UUIDField(primary_key=True, default= uuid.uuid4)
    name= models.CharField(max_length=255)

    def __str__(self):
        return self.name

class ChatModel(models.Model):
    sent_by= models.CharField(max_length=200, null=True, blank=True)
    chat_id= models.UUIDField(primary_key=True, default=uuid.uuid4)
    messages= models.CharField(max_length=1000)
    timestamp= models.DateTimeField(auto_now_add=True)
    group= models.ForeignKey(GroupModel, related_name='group_chats', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.messages


class Coin(models.Model):
    class Meta:
        ordering= ['-created_at']

    coin_id= models.UUIDField(primary_key=True, default=uuid.uuid4)
    owner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    # amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    hash = models.CharField(max_length=256)
    prev_coin = models.ForeignKey('self', related_name='next_coin_reverse', on_delete=models.SET_NULL, null=True, blank=True)
    next_coin = models.ForeignKey('self', related_name='prev_coin_reverse', on_delete=models.SET_NULL, null=True, blank=True)

    def delete(self, using=None, keep_parents=False):
        # raise NotImplementedError("Deletion of Coin objects is not allowed")
        pass

    def save(self, *args, **kwargs):
        # Generate hash using user's username and current timestamp
        string_to_hash = f"{self.owner.email}-{self.created_at}"
        hash_object = hashlib.sha256(string_to_hash.encode())
        hash_hex = hash_object.hexdigest()
        # Save the hash to the model instance
        self.hash = hash_hex
        if not Coin.objects.exists():
            self.prev_coin= None

        super().save(*args, **kwargs)

class Transaction(models.Model):
    class Meta:
        ordering= ['coin','-created_at']
    transaction_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    sender = models.ForeignKey(CustomUser, on_delete=models.SET_NULL,null=True,blank=True, related_name='sender')
    receiver = models.ForeignKey(CustomUser, on_delete=models.SET_NULL,null=True,blank=True, related_name='receiver')
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE, null=True,blank=True)
    amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    hash = models.CharField(max_length=256)
    prev_transaction= models.ForeignKey('self', related_name='next_transaction_reverse', on_delete=models.SET_NULL, null=True, blank=True)
    next_transaction= models.ForeignKey('self', related_name='prev_transaction_reverse', on_delete=models.SET_NULL, null=True, blank=True)

    def generate_hash(self, previous_hash=None):
        if self.sender is None:
            string_to_hash = f"{self.sender}-{self.receiver.email}-{self.amount}-{self.created_at}"
        else:
            string_to_hash = f"{self.sender.email}-{self.receiver.email}-{self.amount}-{self.created_at}"
        if previous_hash:
            string_to_hash = f"{previous_hash}-{string_to_hash}"
        hash_object = hashlib.sha256(string_to_hash.encode())
        return hash_object.hexdigest()
    
    def save(self, *args, **kwargs):
        previous_transaction = Transaction.objects.filter(coin=self.coin).order_by('-created_at').first()
        previous_hash = previous_transaction.hash if previous_transaction else None
        self.hash = self.generate_hash(previous_hash)
        super().save(*args, **kwargs)