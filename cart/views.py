from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Cart
from products.models import Product


# ==========================
# Add Product To Cart
# ==========================

def add_to_cart(request, product_id):

    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key

    product = get_object_or_404(Product, id=product_id)

    # Stock Check
    if product.stock <= 0:

        messages.error(
            request,
            "This product is Out Of Stock."
        )

        return redirect("home")

    cart_item = Cart.objects.filter(
        product=product,
        session_key=session_key
    ).first()

    if cart_item:

        if cart_item.quantity < product.stock:

            cart_item.quantity += 1

            cart_item.save()

        else:

            messages.warning(

                request,

                "Maximum stock reached."

            )

    else:

        Cart.objects.create(

            product=product,

            quantity=1,

            session_key=session_key

        )

    return redirect("cart")


# ==========================
# Cart Page
# ==========================

def cart(request):

    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key

    cart_items = Cart.objects.filter(
        session_key=session_key
    )

    total = 0

    for item in cart_items:

        total += item.total_price

    context = {

        "cart_items": cart_items,

        "total": total

    }

    return render(

        request,

        "cart.html",

        context

    )


# ==========================
# Increase Quantity
# ==========================

def increase_quantity(request, cart_id):

    cart_item = get_object_or_404(
        Cart,
        id=cart_id
    )

    if cart_item.quantity < cart_item.product.stock:

        cart_item.quantity += 1

        cart_item.save()

    else:

        messages.warning(

            request,

            "No more stock available."

        )

    return redirect("cart")


# ==========================
# Decrease Quantity
# ==========================

def decrease_quantity(request, cart_id):

    cart_item = get_object_or_404(
        Cart,
        id=cart_id
    )

    if cart_item.quantity > 1:

        cart_item.quantity -= 1

        cart_item.save()

    else:

        cart_item.delete()

    return redirect("cart")


# ==========================
# Remove Item
# ==========================

def remove_cart_item(request, cart_id):

    cart_item = get_object_or_404(
        Cart,
        id=cart_id
    )

    cart_item.delete()

    messages.success(

        request,

        "Product Removed From Cart."

    )

    return redirect("cart")