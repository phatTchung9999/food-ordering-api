from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Category, MenuItem, Cart, Order, OrderItem
from .serializers import CategorySerializer, MenuItemSerializer, CartSerializer, OrderSerializer, UserSerializer
from rest_framework.response import Response

from rest_framework.permissions import IsAdminUser
from django.shortcuts import  get_object_or_404

from django.contrib.auth.models import Group, User

from rest_framework.viewsets import ViewSet
from rest_framework import status


class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    search_fields = ['category__title']
    ordering_fields = ['price', 'inventory']

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

class CartView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Cart.objects.all()
        return Cart.objects.all().filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        Cart.objects.all().filter(user=self.request.user).delete()
        return Response("ok")


class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.all()
        elif self.request.user.groups.count()==0: 
            return Order.objects.all().filter(user=self.request.user)
        elif self.request.user.groups.filter(name='Delivery Crew').exists(): 
            return Order.objects.all().filter(delivery_crew=self.request.user)
        else:
            return Order.objects.all()


    def create(self, request, *args, **kwargs):
        menuitem_count = Cart.objects.all().filter(user=self.request.user).count()
        if menuitem_count == 0:
            return Response({"message:": "no item in cart"})

        data = request.data.copy()
        total = self.get_total_price(self.request.user)
        # data['total'] = total
        data['user'] = self.request.user.id
        order_serializer = OrderSerializer(data=data)
        if order_serializer.is_valid():
            order = order_serializer.save(
                total=total
            )

            items = Cart.objects.all().filter(user=self.request.user).all()

            for item in items.values():
                orderitem = OrderItem(
                    order=order,
                    menuitem_id=item['menuitem_id'],
                    price=item['price'],
                    quantity=item['quantity'],
                )
                orderitem.save()

            Cart.objects.all().filter(user=self.request.user).delete() 

            result = order_serializer.data.copy()
            result['total'] = total
            return Response(order_serializer.data)
    
    def get_total_price(self, user):
        total = 0
        items = Cart.objects.all().filter(user=user).all()
        for item in items.values():
            total += item['price']
        return total

class SingleOrderView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        if self.request.user.groups.filter(name='Delivery Crew').exists():
            return Order.objects.all().filter(delivery_crew=self.request.user)
        elif self.request.user.groups.filter(name='Manager') or self.request.user.is_superuser:
            return Order.objects.all()

    def delete(self, request, *args, **kwargs):
        if not self.request.user.groups.filter(name='Manager').exists() or not self.request.user.is_superuser():
            return Response({'message': 'You do not have the permission.'}, status=status.HTTP_403_FORBIDDEN)
        return super().delete(request, *args, **kwargs)

class GroupViewSet(ViewSet):
    permission_classes = [IsAdminUser]
    def list(self, request):
        users = User.objects.all().filter(groups__name='Manager')
        items = UserSerializer(users, many=True)
        return Response(items.data)
    
    def create(self, request):
        user = get_object_or_404(User, username=request.data['username'])
        managers = Group.objects.get(name='Manager')
        managers.user_set.add(user)
        return Response(
            {'message': 'user added to the manager group.'}, status=status.HTTP_201_CREATED
        )

    def destroy(self, request, pk=None):
        # user = get_object_or_404(User, pk=pk)
        managers = Group.objects.get(name='Manager')
        user = get_object_or_404(User, pk=pk, groups__name='Manager')        
        managers.user_set.remove(user)
        return Response(
            {'message': 'user deleted from the manager group.'}, status=status.HTTP_200_OK
        )

class DeliveryCrewViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    def list(self, request):
        users = User.objects.all().filter(groups__name='Delivery Crew')
        items = UserSerializer(users, many=True)
        return Response(items.data)
    
    def create(self, request):
        if self.request.user.groups.filter(name='Manager').exists() or self.request.user.is_superuser:
            user = get_object_or_404(User, username=request.data['username'])
            delivery_crew = Group.objects.get(name='Delivery Crew')
            delivery_crew.user_set.add(user)
            return Response(
                {'message': 'user added to the delivery group.'}, status=status.HTTP_201_CREATED
            )
        else: 
            return Response({"message":"forbidden"}, status.HTTP_403_FORBIDDEN)
    def destroy(self, request, pk=None):
        if self.request.user.groups.filter(name='Manager').exists() or self.request.user.is_superuser:
            # user = get_object_or_404(User, pk=pk)
            delivery_crew = Group.objects.get(name='Delivery Crew')
            user = get_object_or_404(User, pk=pk, groups__name='Delivery Crew')
            delivery_crew.user_set.remove(user)
            return Response(
                {'message': 'user deleted from the delivery group.'}, status=status.HTTP_200_OK
            )
        else:
            return Response({"message":"forbidden"}, status.HTTP_403_FORBIDDEN)