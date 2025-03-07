from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from .views import UserListView, user_register, user_login, user_logout, UserUpdateView

urlpatterns = [
    path('api/', UserListView.as_view(), name='user-list'),
    path('api/register/', user_register, name='register'),
    path('api/login/', user_login, name='login') , 
    path('api/logout/', user_logout, name='logout'), 
    path('api/users/<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)