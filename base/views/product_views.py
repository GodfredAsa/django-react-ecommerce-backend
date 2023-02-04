from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from base.models import Product, Review
from base.serializers import ProductSerializer

@api_view(['GET'])
def getProducts(request):
    query = request.query_params.get('keyword')
    if query == None:
        query = ''
    products = Product.objects.filter(name__icontains = query)
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
@permission_classes([IsAdminUser])
def uploadProductImage(request):
    data = request.data 
    product_id = data['product_id']
    product = Product.objects.get(_id=product_id)
    product.image = request.FILES.get('image')
    product.save()
    Response({'details':'Image Uploaded Successfully'}, status=status.HTTP_200_OK)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createProductReview(request, pk):
    user = request.user
    product = Product.objects.get(_id = pk)
    data = request.data
    
    # SCENARIOS 
    # 1. review already exists
    alreadyExists = product.review_set.filter(user = user).exists()
    if alreadyExists:
        content = {'detail': 'Product already Reviewed'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    
    # 2 No rating or rating is 0
    elif data['rating'] == 0:
        content = {'detail': 'Please Select a Rating '}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
    # 3 Create review 
    else:
        review = Review.objects.create(
            user = user,
            product = product,
            name = user.first_name,
            rating = data['rating'],
            comment = data['comment']
        )
        
        # we need to update the review of the product of the model
        reviews = product.review_set.all()
        product.numReviews = len(reviews)
         
        total = 0
        for i in reviews:
            total += i.rating
        # calculate rating 
        product.rating = total / len(reviews)
        # save product with review and rating 
        product.save()
        return Response('Review Added Successfully')
    
