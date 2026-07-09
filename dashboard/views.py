from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User

from products.models import Product, Category
from orders.models import Order
from reviews.models import Review
from wishlist.models import Wishlist

from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages

from django.core.paginator import Paginator

from .forms import ProductForm
@staff_member_required
def dashboard(request):

    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    total_users = User.objects.count()
    total_orders = Order.objects.exclude(status="Cancelled").count()
    cancelled_orders = Order.objects.filter(status="Cancelled").count()
    total_reviews = Review.objects.count()
    total_wishlist = Wishlist.objects.count()

    total_sales = sum(order.total for order in Order.objects.exclude(status="Cancelled"))

    latest_orders = Order.objects.order_by("-created_at")[:5]

    recent_users = User.objects.order_by("-date_joined")[:5]

    low_stock_products = Product.objects.filter(
        stock__lt=5
    ).order_by("stock")

    pending_orders = Order.objects.filter(status="Pending").count()

    processing_orders = Order.objects.filter(status="Processing").count()

    delivered_orders = Order.objects.filter(status="Delivered").count()

    context = {

        "total_products": total_products,
        "total_categories": total_categories,
        "total_users": total_users,
        "total_orders": total_orders,
        "total_reviews": total_reviews,
        "total_wishlist": total_wishlist,
        "total_sales": total_sales,

        "latest_orders": latest_orders,
        "recent_users": recent_users,
        "low_stock_products": low_stock_products,

        "pending_orders": pending_orders,
        "processing_orders": processing_orders,
        "delivered_orders": delivered_orders,

    }

    return render(
        request,
        "dashboard/dashboard.html",
        context
    )




# ================================================
# Product List
# ================================================

@staff_member_required
def product_list(request):

    search = request.GET.get("search")

    products = Product.objects.all().order_by("-id")

    if search:

        products = products.filter(

            name__icontains=search

        )

    paginator = Paginator(

        products,

        10

    )

    page = request.GET.get("page")

    products = paginator.get_page(page)

    return render(

        request,

        "dashboard/product_list.html",

        {

            "products": products,

            "search": search

        }

    )


# ================================================
# Add Product
# ================================================

@staff_member_required
def add_product(request):

    if request.method == "POST":

        form = ProductForm(

            request.POST,

            request.FILES

        )

        if form.is_valid():

            form.save()

            messages.success(

                request,

                "Product Added Successfully."

            )

            return redirect(

                "product_list"

            )

    else:

        form = ProductForm()

    return render(

        request,

        "dashboard/add_product.html",

        {

            "form": form

        }

    )


# ================================================
# Edit Product
# ================================================

@staff_member_required
def edit_product(request, id):

    product = get_object_or_404(

        Product,

        id=id

    )

    if request.method == "POST":

        form = ProductForm(

            request.POST,

            request.FILES,

            instance=product

        )

        if form.is_valid():

            form.save()

            messages.success(

                request,

                "Product Updated Successfully."

            )

            return redirect(

                "product_list"

            )

    else:

        form = ProductForm(

            instance=product

        )

    return render(

        request,

        "dashboard/edit_product.html",

        {

            "form": form,

            "product": product

        }

    )


# ================================================
# Delete Product
# ================================================

@staff_member_required
def delete_product(request, id):

    product = get_object_or_404(

        Product,

        id=id

    )

    product.delete()

    messages.success(

        request,

        "Product Deleted Successfully."

    )

    return redirect(

        "product_list"

    )