from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from django.core.mail import send_mail
from django.conf import settings

from cart.models import Cart
from .models import Order
from .forms import OrderStatusForm, CheckoutForm


# ==========================
# Customer Checkout
# ==========================

@login_required
def checkout(request):

    session_key = request.session.session_key

    if not session_key:

        request.session.create()

        session_key = request.session.session_key

    cart_items = Cart.objects.filter(
        session_key=session_key
    )

    if not cart_items.exists():

        messages.warning(
            request,
            "Your cart is empty."
        )

        return redirect("cart")

    # Stock Check

    for item in cart_items:

        if item.product.stock < item.quantity:

            messages.error(

                request,

                f"Only {item.product.stock} item(s) available for {item.product.name}."

            )

            return redirect("cart")

    # ==========================
    # Checkout Form
    # ==========================

    if request.method == "POST":

        form = CheckoutForm(request.POST)

        if form.is_valid():

            data = form.cleaned_data

            for item in cart_items:

                order = Order.objects.create(

                    user=request.user,

                    product=item.product,

                    quantity=item.quantity,

                    price=item.product.price,

                    total=item.total_price,

                    full_name=data["full_name"],

                    phone=data["phone"],

                    email=data["email"],

                    address=data["address"],

                    city=data["city"],

                    state=data["state"],

                    pincode=data["pincode"],

                    country=data["country"]

                )

                # Reduce Stock

                item.product.stock -= item.quantity

                item.product.save()

                # Email

                if data["email"]:

                    subject = f"Order Confirmed - {order.invoice_no}"

                    message = f"""
Hello {data['full_name']},

Your Order has been placed successfully.

Invoice No : {order.invoice_no}

Product : {order.product.name}

Quantity : {order.quantity}

Total : ₹{order.total}

Delivery Address:

{order.address}

{order.city}, {order.state}

{order.pincode}

{order.country}

Status : {order.status}

Thank You For Shopping.
"""

                    try:

                        send_mail(

                            subject,

                            message,

                            settings.DEFAULT_FROM_EMAIL,

                            [data["email"]],

                            fail_silently=False

                        )

                    except Exception as e:

                        print(e)

            cart_items.delete()

            messages.success(

                request,

                "Order Placed Successfully."

            )

            return redirect("my_orders")

    else:

        form = CheckoutForm(

            initial={

                "full_name": request.user.get_full_name(),

                "email": request.user.email,

                "country": "India"

            }

        )

    return render(

        request,

        "orders/checkout.html",

        {

            "form": form,

            "cart_items": cart_items,

            "total": sum(item.total_price for item in cart_items)

        }

    )


# ==========================
# Customer Orders
# ==========================

@login_required
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(

        request,

        "my_orders.html",

        {

            "orders": orders

        }

    )


# ==========================
# Admin Orders
# ==========================

@staff_member_required
def admin_orders(request):

    search = request.GET.get("search")

    orders = Order.objects.all().order_by(
        "-created_at"
    )

    if search:

        orders = orders.filter(
            invoice_no__icontains=search
        )

    return render(

        request,

        "orders/admin_orders.html",

        {

            "orders": orders,

            "search": search

        }

    )


# ==========================
# Order Detail
# ==========================

@staff_member_required
def order_detail(request, pk):

    order = get_object_or_404(

        Order,

        pk=pk

    )

    if request.method == "POST":

        form = OrderStatusForm(

            request.POST,

            instance=order

        )

        if form.is_valid():

            form.save()

            messages.success(

                request,

                "Order Status Updated Successfully."

            )

            return redirect(

                "admin_orders"

            )

    else:

        form = OrderStatusForm(

            instance=order

        )

    return render(

        request,

        "orders/order_detail.html",

        {

            "order": order,

            "form": form

        }

    )


# ==========================
# Invoice
# ==========================

@login_required
def invoice(request, pk):

    order = get_object_or_404(

        Order,

        pk=pk,

        user=request.user

    )

    return render(

        request,

        "orders/invoice.html",

        {

            "order": order

        }

    )


# ==========================
# Delete Order
# ==========================

@staff_member_required
def delete_order(request, pk):

    order = get_object_or_404(

        Order,

        pk=pk

    )

    order.delete()

    messages.success(

        request,

        "Order Deleted Successfully."

    )

    return redirect(

        "admin_orders"

    )




@login_required
def cancel_order(request, pk):

    order = get_object_or_404(
        Order,
        pk=pk,
        user=request.user
    )

    if order.status != "Pending":

        messages.error(
            request,
            "Only Pending Orders can be cancelled."
        )

        return redirect("my_orders")

    # Stock wapas add karo
    order.product.stock += order.quantity
    order.product.save()

    order.status = "Cancelled"
    order.save()

    messages.success(
        request,
        "Order Cancelled Successfully."
    )

    return redirect("my_orders")


@login_required
def track_order(request, pk):

    order = get_object_or_404(

        Order,

        pk=pk,

        user=request.user

    )

    return render(

        request,

        "orders/tracking.html",

        {

            "order": order

        }

    )