from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from orders.cart import Cart
from products.models import Product


class CartView(TemplateView):
    template_name = 'orders/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = Cart(self.request)
        return context


class CartAddView(TemplateView):
    NEW_PRODUCT = True
    template_name = 'orders/cart.html'

    def post(self, request, *args, **kwargs):
        next = request.POST.get('next', reverse('products:product_details'))

        product_slug = request.POST.get('product_slug')
        product = Product.objects.get(slug=product_slug)
        quantity = int(request.POST.get('quantity', 1))
        cart = Cart(request)
        if self.NEW_PRODUCT:
            cart.add(product, quantity)
        else:
            cart.set_quantity(product, quantity)
        return redirect(next, slug=product.slug)


class CartUpdateView(CartAddView):
    NEW_PRODUCT = False


class CartRemoveView(TemplateView):
    template_name = 'orders/cart.html'

    def post(self, request, *args, **kwargs):
        product_slug = request.POST.get('product_slug')
        product = Product.objects.get(slug=product_slug)
        cart = Cart(request).remove(product)
        return redirect('orders:cart')
