from django.views.generic import ListView, TemplateView

from products.models import Product


class ProductList(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'


class GuidesRecipesView(TemplateView):
    template_name = 'products/guides-recipes.html'
