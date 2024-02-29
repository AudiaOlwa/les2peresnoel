from django.forms import ModelForm

from .models import Category, Product


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        exclude = ("id", "created", "updated", "slug")


class ProductForm(ModelForm):
    class Meta:
        model = Product
        exclude = ("id", "created", "updated", "slug")
