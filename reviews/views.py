from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Review
from products.models import Product


@login_required
def add_review(request, product_id):

    if request.method == "POST":

        product = get_object_or_404(
            Product,
            id=product_id
        )

        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        Review.objects.create(

            product=product,
            user=request.user,
            rating=rating,
            comment=comment

        )

    return redirect("product_detail", id=product.id)