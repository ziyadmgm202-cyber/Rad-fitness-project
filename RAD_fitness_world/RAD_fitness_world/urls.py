
from django.contrib import admin
from django.urls import path,include
from shop import views
app_name = 'ecommerce'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    path('cart/', include('cart.urls')),
    path('search/', include('search.urls')),
]
from django.conf.urls.static import static
from django.conf import settings

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)