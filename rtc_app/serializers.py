from rest_framework import serializers
from .models import GroupModel

class ListGroupModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupModel
        fields = ['name', 'picture', 'slug']

# class CreateGroupModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = GroupModel
#         fields = ['name', 'picture', 'slug']