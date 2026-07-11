from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Q

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from django.core.mail import send_mail
from django.conf import settings

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from io import BytesIO
from datetime import datetime

from cart.models import Cart
from .models import Order
from .forms import OrderStatusForm, CheckoutForm, CancelOrderForm


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

from django.db.models import Q
from datetime import datetime


@staff_member_required
def admin_orders(request):

    search = request.GET.get("search", "")
    date = request.GET.get("date", "")

    orders = Order.objects.all().order_by("-created_at")

    # Search by invoice, username, product
    if search:

        orders = orders.filter(

            Q(invoice_no__icontains=search) |
            Q(user__username__icontains=search) |
            Q(product__name__icontains=search)

        )

    # Search by date
    if date:

        try:

            selected_date = datetime.strptime(date, "%Y-%m-%d").date()

            orders = orders.filter(
                created_at__date=selected_date
            )

        except ValueError:

            pass

    return render(

        request,

        "orders/admin_orders.html",

        {

            "orders": orders,
            "search": search,
            "date": date,

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
# Download Invoice PDF
# ==========================

@login_required
def download_invoice(request, pk):

    order = get_object_or_404(
        Order,
        pk=pk,
        user=request.user
    )

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Invoice_{order.invoice_no}.pdf"'

    # Create PDF document
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#333333'),
        spaceAfter=12,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6,
    )
    
    # Add title
    title = Paragraph("INVOICE", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.3*inch))
    
    # Store info and customer info
    data = [
        [
            Paragraph("<b>E-Commerce Store</b>", heading_style),
            Paragraph("<b>Customer Details</b>", heading_style)
        ],
        [
            Paragraph("123 Main Market<br/>Bhopal, India<br/>support@ecommerce.com", normal_style),
            Paragraph(f"Name: {order.full_name}<br/>Email: {order.email}<br/>Phone: {order.phone}", normal_style)
        ]
    ]
    
    store_table = Table(data, colWidths=[3.25*inch, 3.25*inch])
    store_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    
    elements.append(store_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Invoice details
    invoice_details = [
        [
            Paragraph(f"<b>Invoice No:</b> {order.invoice_no}", normal_style),
            Paragraph(f"<b>Order Date:</b> {order.created_at.strftime('%d-%m-%Y')}", normal_style),
            Paragraph(f"<b>Status:</b> {order.status}", normal_style)
        ]
    ]
    
    details_table = Table(invoice_details, colWidths=[2.1*inch, 2.1*inch, 2.1*inch])
    details_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    
    elements.append(details_table)
    elements.append(Spacer(1, 0.2*inch))
    
    # Delivery address
    elements.append(Paragraph("<b>Delivery Address</b>", heading_style))
    address_text = f"{order.address}<br/>{order.city}, {order.state}<br/>{order.pincode}<br/>{order.country}"
    elements.append(Paragraph(address_text, normal_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Order items table
    elements.append(Paragraph("<b>Order Details</b>", heading_style))
    
    items_data = [
        ['Product', 'Price', 'Quantity', 'Total']
    ]
    
    items_data.append([
        Paragraph(order.product.name, normal_style),
        Paragraph(f"₹{order.price}", normal_style),
        Paragraph(str(order.quantity), normal_style),
        Paragraph(f"₹{order.total}", normal_style)
    ])
    
    items_table = Table(items_data, colWidths=[2.5*inch, 1.3*inch, 1.3*inch, 1.3*inch])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
    ]))
    
    elements.append(items_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Total table
    total_data = [
        ['Sub Total', f'₹{order.total}'],
        ['Shipping', '₹0.00'],
        ['Tax', '₹0.00'],
        ['Grand Total', f'₹{order.total}']
    ]
    
    total_table = Table(total_data, colWidths=[5.2*inch, 1.3*inch])
    total_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 3), (-1, 3), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 2), 10),
        ('FONTSIZE', (0, 3), (-1, 3), 12),
        ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor('#1f4788')),
        ('TEXTCOLOR', (0, 3), (-1, 3), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('RIGHTPADDING', (0, 0), (-1, -1), 20),
    ]))
    
    elements.append(total_table)
    elements.append(Spacer(1, 0.5*inch))
    
    # Footer
    footer_text = "Thank You For Shopping! Please keep this invoice for your records. For any queries, contact support@ecommerce.com"
    elements.append(Paragraph(footer_text, normal_style))
    
    # Build PDF
    doc.build(elements)
    
    # Get PDF data
    pdf_buffer.seek(0)
    response.write(pdf_buffer.read())
    
    return response


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

    if request.method == "POST":

        form = CancelOrderForm(request.POST, instance=order)

        if form.is_valid():

            order.product.stock += order.quantity
            order.product.save()

            order.status = "Cancelled"
            order.cancel_reason = form.cleaned_data["cancel_reason"]
            order.save()

            messages.success(
                request,
                "Order Cancelled Successfully."
            )

            return redirect("my_orders")

    else:

        form = CancelOrderForm()

    return render(
        request,
        "orders/cancel_order.html",
        {
            "order": order,
            "form": form
        }
    )


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