from rest_framework import generics
from .models import GroupModel
from .serializers import ListGroupModelSerializer

# class GroupCreateAPIView(generics.CreateAPIView):
#     queryset = GroupModel.objects.all()
#     serializer_class = CreateGroupModelSerializer

class GroupListAPIView(generics.ListAPIView):
    queryset = GroupModel.objects.all()
    serializer_class = ListGroupModelSerializer