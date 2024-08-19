from django.forms import ModelForm, widgets

from .models import Category, Product, ProductImage, Checkout


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