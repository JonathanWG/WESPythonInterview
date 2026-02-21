from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('Users.urls')),
    path('api/payments/', include('paymentProcess.urls')),
    path('api/feed/', include('feed.urls')),
]