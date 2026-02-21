from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('Users.urls')),
    path('api/payments/', include('PaymentProcess.urls')),
    path('api/feed/', include('Feed.urls')),
]