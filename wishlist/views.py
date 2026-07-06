from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Wishlist
from products.models import Product


@login_required
def add_to_wishlist(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    return redirect("my_wishlist")


@login_required
def my_wishlist(request):

    wishlist = Wishlist.objects.filter(
        user=request.user
    )

    return render(
        request,
        "my_wishlist.html",
        {
            "wishlist": wishlist
        }
    )


@login_required
def remove_wishlist(request, id):

    item = get_object_or_404(
        Wishlist,
        id=id,
        user=request.user
    )

    item.delete()

    return redirect("my_wishlist")