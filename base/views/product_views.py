from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from base.models import Product
from base.serializers import ProductSerializer

@api_view(['GET'])
def getProducts(request):
    products = [ product for product in Product.objects.all() if product.countInStock > 0]
    serializer = ProductSerializer(products, many = True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def getProduct(request, pk):
    product = Product.objects.get(_id=pk)
    serializer = ProductSerializer(product, many = False)
    return  Response(serializer.data, status=status.HTTP_200_OK)  

@api_view(['POST'])
@permission_classes([IsAdminUser])
def createProduct(request):
    user = request.user
    product = Product.objects.create(
        user = user,
        name = "Sample Name",
        price = 0,
        brand = "Sample Brand",
        countInStock = 1,
        category = "Sample Category",
        description = "description"  
    )
    serializer = ProductSerializer(product, many = False)
    return  Response(serializer.data, status=status.HTTP_201_CREATED) 

@api_view(['PUT'])
def updateProduct(request, pk):
    data = request.data
    product = Product.objects.get(_id=pk)
    product.name = data['name']
    product.price = data['price']
    product.brand = data['brand']
    product.category = data['category']
    product.countInStock = data['countInStock']
    product.description = data['description']
    product.save()
    serializer = ProductSerializer(product, many = False)
    return  Response(serializer.data, status=status.HTTP_200_OK)   

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteProduct(request, pk):
    product = Product.objects.get(_id=pk)
    if not product:
        return Response({"details": f"Product With ID {pk} Not Found"}, status=status.HTTP_404_NOT_FOUND)
    product.delete()
    return Response({'details': 'Product successfully deleted'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def uploadProductImage(request):
    data = request.data 
    product_id = data['product_id']
    product = Product.objects.get(_id=product_id)
    product.image = request.FILES.get('image')
    product.save()
    Response({'details':'Image Uploaded Successfully'}, status=status.HTTP_200_OK)
