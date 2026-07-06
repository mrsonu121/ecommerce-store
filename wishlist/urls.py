from django.urls import path
from . import views

urlpatterns = [

    path(
        "add/<int:product_id>/",
        views.add_to_wishlist,
        name="add_to_wishlist"
    ),

    path(
        "",
        views.my_wishlist,
        name="my_wishlist"
    ),

    path(
        "remove/<int:id>/",
        views.remove_wishlist,
        name="remove_wishlist"
    ),

]