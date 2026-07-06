from django import forms

from products.models import Product


class ProductForm(forms.ModelForm):

    class Meta:

        model = Product

        fields = [

            "category",

            "name",

            "price",

            "description",

            "image",

            "stock"

        ]

        widgets = {

            "category": forms.Select(

                attrs={

                    "class": "form-select"

                }

            ),

            "name": forms.TextInput(

                attrs={

                    "class": "form-control",

                    "placeholder": "Product Name"

                }

            ),

            "price": forms.NumberInput(

                attrs={

                    "class": "form-control",

                    "placeholder": "Price"

                }

            ),

            "description": forms.Textarea(

                attrs={

                    "class": "form-control",

                    "rows": 4,

                    "placeholder": "Product Description"

                }

            ),

            "image": forms.FileInput(

                attrs={

                    "class": "form-control"

                }

            ),

            "stock": forms.NumberInput(

                attrs={

                    "class": "form-control",

                    "placeholder": "Stock"

                }

            ),

        }