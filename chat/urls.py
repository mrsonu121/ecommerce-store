from django.urls import path
from . import views

urlpatterns = [

    path("", views.customer_chat, name="customer_chat"),

    path("admin/", views.admin_chat, name="admin_chat"),

]