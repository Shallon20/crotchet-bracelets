from my_app.models import Product
class Cart():
    def __init__(self, request):
        self.session = request.session

        # Get the current session key if it exists
        cart = self.session.get('session_key')

        # If the user is new, no session key, create one
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # make sure cart is available in all pages of the site
        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty =str(quantity)
        # logic
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

    def __len__(self):
        return len(self.cart)

    def get_prods(self):
        #get ids from cart
        product_ids = self.cart.keys()
        # use ids to lookup products in database model
        products = Product.objects.filter(id__in=product_ids)
        # return looked up products
        return products

    def get_quants(self):
        quantities = self.cart
        return quantities

    def update(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        #get cart
        ourcart = self.cart
        #update dictionary/cart
        ourcart[product_id] = product_qty

        self.session.modified = True
        thing = self.cart
        return thing

    def delete(self, product):
        product_id = str(product.id)
        # delete from dictionary/cart
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

    def cart_total(self):
        # get product ids
        product_ids = self.cart.keys()
        #lookup those keys in our product database model
        products = Product.objects.filter(id__in=product_ids)
        # get quantities
        quantities = self.cart
        # start counting at 0
        total = 0
        for key, value in quantities.items():
            # convert string to int so that we can do the math
            key = int(key)
            for product in products:
                if product.id == key:
                    total = total + (product.price * value)

            return total