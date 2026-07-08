from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('admin/', admin.site.urls),

    path('', include('products.urls')),

    path('cart/', include('cart.urls')),

    path('accounts/', include('accounts.urls')),

    path('orders/', include('orders.urls')),

    path('wishlist/', include('wishlist.urls')),

    path('reviews/', include('reviews.urls')),

    # ================= Dashboard =================

    path('dashboard/', include('dashboard.urls')),

    
    path('chat/', include('chat.urls')),

]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)