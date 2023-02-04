from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from base.models import Product, Order, OrderItem, ShippingAddress
from base.serializers import ProductSerializer, OrderSerializer
from rest_framework import status
from datetime import datetime


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrderItems(request):
    user = request.user
    data  = request.data 
    orderItems = data['orderItems']
    
    if orderItems and len(orderItems) == 0:
        return Response({'details': "No Order Items"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        # STEPS FOR PROCESSING THE ORDER
        # (1) create order 
        order = Order.objects.create(
            user = user,
            paymentMethod = data['paymentMethod'],
            taxPrice = data['taxPrice'],
            shippingPrice = data['shippingPrice'],
            totalPrice = data['totalPrice'] 
        )
        
        # (2) create shipping address
        shippingAddress = ShippingAddress.objects.create(
            order = order,
            address = data["shippingAddress"]["address"],
            city = data['shippingAddress']['city'],
            postalCode = data['shippingAddress']['postalCode'],
            country = data['shippingAddress']['country'],    
        )
        # (3) create order Items and set the order to orderItem rlnship
        for i in orderItems:
            # setting product orderitem rlnship
            product = Product.objects.get(_id = i['product'])
            item = OrderItem.objects.create(
                product = product,
                order = order,
                name = product.name,
                qty = i['qty'],
                price = i['price'],
                image = product.image.url
            )
        # (4) update stock
        product.countInStock -= int(item.qty)
        product.save()
        serializer = OrderSerializer(order, many = False)
         
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyOrders(request):
    user = request.user
    orders = user.order_set.all()
    serializer = OrderSerializer(orders, many = True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getOrders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many = True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrderById(request, pk):
    user = request.user
    order = Order.objects.get(_id=pk)
    
    # an order can be viewed by the order user and admin.
    try:
        if user.is_staff or order.user == user:
            serializer = OrderSerializer(order, many = False)
            return Response(serializer.data)
        else:
            return Response({'detail': 'Not Authorised to view this Order'}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'detail': 'Order does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated]) 
def updateOrderToPaid(request, pk):
    order  = Order.objects.get(_id=pk)
    order.isPaid = True
    order.paidAt = datetime.now()
    order.save()
    return Response("Order was paid")

@api_view(['PUT'])
@permission_classes([IsAdminUser]) 
def updateOrderToDelivered(request, pk):
    order  = Order.objects.get(_id=pk)
    order.isDelivered = True
    order.deliveredAt = datetime.now()
    order.save()
    return Response("Order was delivered")



