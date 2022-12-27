from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from base.models import Product, Order, OrderItem, ShippingAddress
from base.serializers import ProductSerializer, OrderSerializer
from rest_framework import status


# TODO AM WORKING ON THE ORDERS NOW 
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
                qty = int(i['qty']),
                price = i['price'],
                image = product.image.url
            )
        # (4) update stock
        product.countInStock -= item.qty
        product.save()
        serializer = OrderSerializer(order, many = False)
         
        return Response(serializer.data)
    

