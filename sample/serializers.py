from rest_framework.serializers import ModelSerializer
from sample.models import *


class UserRoleSerializer(ModelSerializer):
    class Meta:
        model =UserRole
        fields = ['title', ]


class UserSerializer(ModelSerializer):
    class Meta:
        model =User
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'role']


class ProductSerializer(ModelSerializer):
    class Meta:
        model =Product
        fields = ['product_name', 'price', ]


class OrderSerializer(ModelSerializer):
    class Meta:
        model =Order
        fields = ['order_id', 'customer', 'vendor', 'order_status', ]

class OrderItemSerializer(ModelSerializer):
    class Meta:
        model =OrderItem
        fields = ['product', 'quantity', 'price', 'order', ]