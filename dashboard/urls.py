from django.urls import path

from . import views


urlpatterns = [

    path(

        "",

        views.dashboard,

        name="dashboard"

    ),

    path(

        "products/",

        views.product_list,

        name="product_list"

    ),

    path(

        "products/add/",

        views.add_product,

        name="add_product"

    ),

    path(

        "products/edit/<int:id>/",

        views.edit_product,

        name="edit_product"

    ),

    path(

        "products/delete/<int:id>/",

        views.delete_product,

        name="delete_product"

    ),

]