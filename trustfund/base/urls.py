from django.urls import  path
from .views import *


urlpatterns = [
    path('user/login/',MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),

    path('user/register/', registerUser, name="register-user"),
    path('user/profile/', getUserProfile, name="profile-user"),
    path('user/vidCount/', increaseVidCount, name='vid-count')

]