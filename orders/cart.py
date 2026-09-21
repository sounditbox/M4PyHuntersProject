from django.http import HttpRequest

from products.models import Product


class Cart:
    CART_SESSION_KEY = 'cart'

    def __init__(self, request: HttpRequest):
        self.session = request.session
        self.session.setdefault(Cart.CART_SESSION_KEY, {})
        self.data: dict[str, int] = self.session[Cart.CART_SESSION_KEY]

    def save(self):
        self.session[Cart.CART_SESSION_KEY] = self.data
        self.session.modified = True

    def set_quantity(self, product: Product, quantity: int):
        self.data[product.slug] = quantity
        self.save()

    def add(self, product: Product, quantity: int):
        self.set_quantity(product, quantity + (self.data.get(product.slug, 0)))
        self.save()

    def remove(self, product: Product):
        self.data.pop(product.slug, None)
        self.save()

    def clear(self):
        self.data.clear()
        self.save()

    def get_items(self):
        return [
            {
                'product_slug': p,
                'quantity': q
            }
            for p, q in self.data.items()
        ]

    def get_quantity(self, product: Product):
        return self.data.get(product.slug, 0)

    @property
    def get_summary(self):
        total = 0
        products = []
        for p, q in self.data.items():
            product = Product.objects.get(slug=p)
            position_product_price = product.price * q
            total += position_product_price
            products.append(
                {
                    'product': product,
                    'quantity': q,
                    'position_price': position_product_price
                }
            )
        return {
            'total': total,
            'products': products
        }
