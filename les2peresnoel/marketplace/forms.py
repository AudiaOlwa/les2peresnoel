from django.forms import ModelForm

from .models import Category, Product, ProductImage


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        exclude = ("id", "created", "updated", "slug")


class ProductForm(ModelForm):
    class Meta:
        model = Product
        exclude = ("id", "created", "updated", "slug")


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
