class Cart:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.setdefault("cart", {})

    def add(self, variant_id, qty):
        key = str(variant_id)
        self.cart[key] = self.cart.get(key, 0) + qty
        self.session.modified = True

    def remove(self, variant_id):
        self.cart.pop(str(variant_id), None)
        self.session.modified = True

    def clear(self):
        self.session["cart"] = {}
        self.session.modified = True

    def items(self):
        from .models import Variant
        ids = self.cart.keys()
        variants = Variant.objects.filter(id__in=ids)
        for v in variants:
            qty = self.cart.get(str(v.id), 0)
            yield v, qty, qty * v.price
