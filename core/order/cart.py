from django.http import Http404
from product.models import ProductVariant


CART_SESSION_ID = 'cart'


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        product_ids = self.cart.keys()
        variants = ProductVariant.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in variants:
            cart[str(product.id)]['product_name'] = product
            cart[str(product.id)]['total_price'] = product.price * cart[str(product.id)]['quantity']
            yield cart[str(product.id)]

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, variant, quantity):
        product_id = str(variant.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(variant.price)}
        self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product_id):
        product_ids = self.cart.keys()
        if str(product_id) in product_ids:
            del self.cart[str(product_id)]
            self.save()
        else:
            raise Http404

    def get_total_price(self):
        return sum(int(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[CART_SESSION_ID]
        self.save()

    def save(self):
        self.session.modified = True

