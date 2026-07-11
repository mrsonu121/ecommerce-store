from django.urls import path
from . import views

urlpatterns = [

    # ==========================
    # Customer
    # ==========================

    path(
        "checkout/",
        views.checkout,
        name="checkout"
    ),

    path(
        "my-orders/",
        views.my_orders,
        name="my_orders"
    ),

    path(
        "invoice/<int:pk>/",
        views.invoice,
        name="invoice"
    ),

    path(
        "invoice/<int:pk>/download/",
        views.download_invoice,
        name="download_invoice"
    ),

    # ==========================
    # Admin
    # ==========================

    path(
        "admin-orders/",
        views.admin_orders,
        name="admin_orders"
    ),

    path(
        "order/<int:pk>/",
        views.order_detail,
        name="order_detail"
    ),

    path(
        "delete-order/<int:pk>/",
        views.delete_order,
        name="delete_order"
    ),


    path(
        "cancel-order/<int:pk>/",
        views.cancel_order,
        name="cancel_order"
    ),
 

    path(
        "track/<int:pk>/",
        views.track_order,
        name="track_order"
    ),
    
]