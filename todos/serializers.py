from .models import List_Task, List_Item
from rest_framework import serializers


class List_Item_Serializer(serializers.ModelSerializer):
    class Meta:
        model = List_Item
        fields = ('list_item_text', 'completed', 'id')

class List_Task_Serializer(serializers.ModelSerializer):
    items = List_Item_Serializer(many = True, read_only = True)
    class Meta:
        model = List_Task
        fields = ('list_task_text', 'pub_date', 'id', 'items')
