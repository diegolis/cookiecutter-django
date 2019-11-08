from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
import django_cas_ng.views as cas_views

urlpatterns = [
    path('service/', include("app.urls")),
    path('accounts/login/', cas_views.LoginView.as_view(), name='cas_ng_login'),
    path('accounts/logout/', cas_views.LogoutView.as_view(), name='cas_ng_logout'),
    path(
        'accounts/callback/',
        cas_views.CallbackView.as_view(),
        name='cas_ng_proxy_callback'
    ),
    path('admin/logout/', cas_views.LogoutView.as_view(), name='cas_ng_logout'),
    path(settings.ADMIN_URL, admin.site.urls),

    # Your stuff: custom urls includes go here

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
