from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from core.views import *
from django.contrib.auth.views import LoginView
# from app_admin.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('shop/', include('items.urls')),
    path('admin_dashboard/', include('admin_dashboard.urls')),
    path('accounts/login/', LoginView.as_view(), name='admin_login'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)