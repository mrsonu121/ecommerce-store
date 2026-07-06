from cart.models import Cart


def cart_count(request):

    count = 0

    # Agar session bana hua hai
    if request.session.session_key:

        count = Cart.objects.filter(
            session_key=request.session.session_key
        ).count()

    return {
        'cart_count': count
    }