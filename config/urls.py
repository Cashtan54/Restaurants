from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from version_1 import views as v1_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', v1_views.RegisterView.as_view(), name='auth_register'),
    path('api/v1/', include('version_1.urls')),
]
