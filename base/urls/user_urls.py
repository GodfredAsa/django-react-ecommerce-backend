from django.urls import path
from base.views import user_views


urlpatterns = [
    path('', user_views.getUsers, name='users'),
    path('<str:pk>', user_views.deleteUser, name='delete-user'),
    path('register', user_views.registerUser, name='register'),
    path('login', user_views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('profile', user_views.getUserProfile, name='users-profile'),    
    path('profile/update', user_views.updateUserProfile, name='update-profile'),
]