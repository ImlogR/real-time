from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(ChatModel)
class ChatModelAdmin(admin.ModelAdmin):
    list_display = ['chat_id', 'messages', 'timestamp', 'group']
    
@admin.register(GroupModel)
class GroupModelAdmin(admin.ModelAdmin):
    list_display = ['group_id', 'name']


@admin.register(Coin)
class CoinAdmin(admin.ModelAdmin):
    list_display= ['coin_id','owner','created_at', 'prev_coin', 'next_coin']
    
    # def has_delete_permission(self, request, obj=None):
    #     return False
    
    def save_model(self, request, obj, form, change):
        # Check if the object has already been saved before
        if obj.pk:
            # Create a new instance with the same details
            last_coin = Coin.objects.order_by('-created_at').first()
            new_coin = Coin(owner=obj.owner, prev_coin=last_coin, next_coin=None)
            new_coin.save()
            last_coin.next_coin= new_coin
            last_coin.save()
            transaction = Transaction.objects.create(sender=None, receiver=obj.owner, coin=new_coin, amount=1)
            transaction.save()
            return

        # If the object hasn't been saved before, save it normally
        super().save_model(request, obj, form, change)

    # def delete_model(self, request, obj):
    #     pass


# admin.site.register(Coin)
# admin.site.register(Transaction)
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display= ['transaction_id','coin', 'sender', 'receiver','prev_transaction','next_transaction', 'amount', 'created_at']

    # def has_delete_permission(self, request, obj=None):
    #         return False
    
        
    def save_model(self, request, obj, form, change):
        # Check if the object has already been saved before
        if obj.pk:
            # Create a new instance with the same details
            related_transaction= Transaction.objects.filter(transaction_id= obj.transaction_id).order_by('-created_at')
            last_transaction = related_transaction.first()
            new_transaction = Transaction(sender=last_transaction.receiver, receiver= obj.receiver, coin= last_transaction.coin, amount= last_transaction.amount, prev_transaction= last_transaction, next_transaction= None)
            if last_transaction.receiver != new_transaction.receiver:
                coin= Coin.objects.get(coin_id= last_transaction.coin.coin_id)
                coin.owner= obj.receiver
                coin.save()
                new_transaction.save()
                last_transaction.next_transaction= new_transaction
                last_transaction.save()
                return
            else:
                pass

        # If the object hasn't been saved before, save it normally
        super().save_model(request, obj, form, change)