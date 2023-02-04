from django.urls import path
from base.views import product_views

urlpatterns = [
    path('', product_views.getProducts, name='products'),
    path('create', product_views.createProduct, name='create-product'),
    path('upload', product_views.uploadProductImage, name='image-upload'),
    
    path('<str:pk>', product_views.getProduct, name='product'),
    path('<str:pk>/review', product_views.createProductReview, name='create-review'),
    
    path('update/<str:pk>', product_views.updateProduct, name='update-product'),
    path('delete/<str:pk>', product_views.deleteProduct, name='product-delete'),
]