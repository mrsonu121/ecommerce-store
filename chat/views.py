from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .models import ChatMessage


# ==========================================
# Customer Chat
# ==========================================

@login_required
def customer_chat(request):

    admin = User.objects.filter(is_superuser=True).first()

    if admin is None:

        messages.error(request, "No admin account found.")

        return redirect("home")

    if request.method == "POST":

        message = request.POST.get("message", "").strip()

        if message:

            ChatMessage.objects.create(

                sender=request.user,

                receiver=admin,

                message=message

            )

            return redirect("customer_chat")

    chats = ChatMessage.objects.filter(

        sender=request.user,
        receiver=admin

    ) | ChatMessage.objects.filter(

        sender=admin,
        receiver=request.user

    )

    chats = chats.order_by("created_at")

    return render(

        request,

        "chat/customer_chat.html",

        {

            "chats": chats,

            "admin": admin

        }

    )


# ==========================================
# Admin Chat
# ==========================================

@login_required
def admin_chat(request):

    if not request.user.is_superuser:

        return redirect("home")

    users = User.objects.filter(

        is_superuser=False

    ).order_by("username")

    selected_user = None

    chats = ChatMessage.objects.none()

    user_id = request.GET.get("user")

    if user_id:

        selected_user = get_object_or_404(

            User,

            id=user_id

        )

        if request.method == "POST":

            message = request.POST.get("message", "").strip()

            if message:

                ChatMessage.objects.create(

                    sender=request.user,

                    receiver=selected_user,

                    message=message

                )

                return redirect(f"/chat/admin/?user={selected_user.id}")

        chats = ChatMessage.objects.filter(

            sender=selected_user,
            receiver=request.user

        ) | ChatMessage.objects.filter(

            sender=request.user,
            receiver=selected_user

        )

        chats = chats.order_by("created_at")

    return render(

        request,

        "chat/admin_chat.html",

        {

            "users": users,

            "selected_user": selected_user,

            "chats": chats

        }

    )