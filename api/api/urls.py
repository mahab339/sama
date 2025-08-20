"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Schema view for Swagger/OpenAPI
def get_swagger_schema():
    return get_schema_view(
        openapi.Info(
            title="Calculator API",
            default_version='v1',
            description="API to calculate interest factors and different economic formulas. It takes the formulas expression as-is, parse it, and calculates the result.",
            terms_of_service="https://sama.up.railway.app/privacy",
            contact=openapi.Contact(email="malmezayen@outlook.com"),
            license=openapi.License(name="GPL License"),
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/', include('calculator.urls')),
    
    # Swagger/OpenAPI documentation
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', get_swagger_schema().without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', get_swagger_schema().with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', get_swagger_schema().with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
