from django.urls import path
from . import views

urlpatterns = [

    # Cart Page
    path('', views.cart, name='cart'),

    # Add Product To Cart
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

    # Increase Quantity
    path('increase/<int:cart_id>/', views.increase_quantity, name='increase_quantity'),

    # Decrease Quantity
    path('decrease/<int:cart_id>/', views.decrease_quantity, name='decrease_quantity'),

    # Remove Product
    path('remove/<int:cart_id>/', views.remove_cart_item, name='remove_cart_item'),

]