from django.forms import ModelForm, widgets, Form, IntegerField, NumberInput

from .models import Category, Product, ProductImage, Checkout

from django.utils.translation import gettext_lazy as _


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        exclude = ("id", "created", "updated", "slug")


class ProductForm(ModelForm):
    class Meta:
        model = Product
        exclude = ("id", "created", "updated", "slug", "is_removed", "owner")
        widgets = {
            "category": widgets.CheckboxSelectMultiple(),
            "description": widgets.Textarea(attrs={"rows": 3}),
        }


class ProductAddForm(Form):
    quantity = IntegerField(
        label=_("Quantité"),
        initial=1,
        min_value=1,
        widget=NumberInput(attrs={"class": "form-control"}),
    )

class ProductImageForm(ModelForm):
    class Meta:
        model = ProductImage
        exclude = (
            "id",
            "created",
            "updated",
        )


class ProductImageSimpleForm(ModelForm):
    class Meta:
        model = ProductImage
        exclude = ("id", "created", "updated", "product")


class CheckoutForm(ModelForm):
    class Meta:
        model = Checkout
        exclude = ('id', 'created', 'updated')