from django import forms
from .models import Order


# ==========================
# Checkout Form
# ==========================

class CheckoutForm(forms.ModelForm):

    class Meta:

        model = Order

        fields = [

            "full_name",

            "phone",

            "email",

            "address",

            "city",

            "state",

            "pincode",

            "country",

        ]

        widgets = {

            "full_name": forms.TextInput(

                attrs={

                    "class": "form-control",

                    "placeholder": "Enter Full Name"

                }

            ),

            "phone": forms.TextInput(

                attrs={

                    "class": "form-control",

                    "placeholder": "Enter Mobile Number"

                }

            ),

            "email": forms.EmailInput(

                attrs={

                    "class": "form-control",

                    "placeholder": "Enter Email"

                }

            ),

            "address": forms.Textarea(

                attrs={

                    "class": "form-control",

                    "rows": 3,

                    "placeholder": "Enter Full Address"

                }

            ),

            "city": forms.TextInput(

                attrs={

                    "class": "form-control",

                    "placeholder": "Enter City"

                }

            ),

            "state": forms.TextInput(

                attrs={

                    "class": "form-control",

                    "placeholder": "Enter State"

                }

            ),

            "pincode": forms.TextInput(

                attrs={

                    "class": "form-control",

                    "placeholder": "Enter Pincode"

                }

            ),

            "country": forms.TextInput(

                attrs={

                    "class": "form-control",

                    "placeholder": "Country"

                }

            ),

        }


# ==========================
# Admin Order Status Form
# ==========================

class OrderStatusForm(forms.ModelForm):

    class Meta:

        model = Order

        fields = [

            "status"

        ]

        widgets = {

            "status": forms.Select(

                attrs={

                    "class": "form-select"

                }

            )

        }


class CancelOrderForm(forms.ModelForm):

    class Meta:

        model = Order

        fields = [

            "cancel_reason"

        ]

        widgets = {

            "cancel_reason": forms.Textarea(

                attrs={

                    "class": "form-control",

                    "rows": 4,

                    "placeholder": "Please tell us why you are cancelling this order."

                }

            )

        }