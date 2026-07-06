from django.shortcuts import render, get_object_or_404
from django.db.models import Avg

from .models import Product, Category
from reviews.models import Review


# ==========================
# Home Page
# ==========================
def home(request):

    query = request.GET.get("q")
    category_id = request.GET.get("category")

    products = Product.objects.all().order_by("-created_at")

    categories = Category.objects.all()

    if query:
        products = products.filter(
            name__icontains=query
        )

    if category_id:
        products = products.filter(
            category_id=category_id
        )

    context = {
        "products": products,
        "categories": categories,
        "query": query,
        "selected_category": category_id,
    }

    return render(
        request,
        "home.html",
        context
    )


# ==========================
# Product Detail
# ==========================
def product_detail(request, id):

    product = get_object_or_404(
        Product,
        id=id
    )

    reviews = Review.objects.filter(
        product=product
    ).order_by("-created_at")

    average_rating = reviews.aggregate(
        Avg("rating")
    )["rating__avg"]

    # Related Products
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(
        id=product.id
    )[:4]

    context = {
        "product": product,
        "reviews": reviews,
        "average_rating": average_rating,
        "related_products": related_products,
    }

    return render(
        request,
        "product_detail.html",
        context
    )