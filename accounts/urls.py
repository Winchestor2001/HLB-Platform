from django.urls import path
from .views import MyTokenObtainPairView, RegistrationAPIView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('register/', RegistrationAPIView.as_view(), name='registration'),

]
