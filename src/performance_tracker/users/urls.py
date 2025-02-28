from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from .views import UserListView, RegisterUserView, CustomTokenObtainPairView, LogoutView, UserUpdateView

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    path('api/', UserListView.as_view(), name='user-list'),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('auth/google/', include('allauth.socialaccount.urls')),
    path('api/register/', RegisterUserView.as_view(), name='register'),
    path('api/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair') , 
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    path('api/logout/', LogoutView.as_view(), name='logout'), 
    path('api/users/<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)