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


def chat_notifications(request):

    unread_count = 0

    if request.user.is_authenticated:

        from chat.models import ChatMessage

        unread_count = ChatMessage.objects.filter(
            receiver=request.user,
            is_read=False
        ).count()

    return {
        'chat_notifications': unread_count
    }