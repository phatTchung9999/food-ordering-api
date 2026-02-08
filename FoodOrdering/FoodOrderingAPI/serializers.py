from rest_framework import serializers
from django.contrib.auth.models import User
from decimal import Decimal

from .models import Category, MenuItem, Cart, Order, OrderItem


class CategorySerializer (serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug']


class MenuItemSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'category', 'featured']


class CartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )

    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)


    def validate(self, attrs):
        menuitem = attrs['menuitem']
        quantity = attrs['quantity']
        attrs['unit_price'] = menuitem.price
        attrs['price'] = attrs['unit_price'] * quantity
        return attrs

    class Meta:
        model = Cart
        fields = ['user', 'menuitem', 'unit_price', 'quantity', 'price']
        extra_kwargs = {
            'price': {'read_only': True}
        }


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['order', 'menuitem', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):

    orderitem = OrderItemSerializer(many=True, read_only=True, source='order')
    total = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew',
                  'status', 'date', 'total', 'orderitem']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email']