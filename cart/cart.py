from venv import logger

from my_app.models import Product, Profile


class Cart:
    def __init__(self, request):
        self.session = request.session
        # get request
        self.request = request

        # Get the current session key if it exists
        cart = self.session.get('session_key')

        # If the user is new, no session key, create one
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # make sure cart is available in all pages of the site
        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        # logic
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True
        # deal with logged in user
        if self.request.user.is_authenticated:
            # get current user
            current_user = Profile.objects.filter(user__id=self.request.user.id)
             # convert single quotes to double quotes
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            #save carty to profile model
            current_user.update(old_cart=str(carty))


    def __len__(self):
        return len(self.cart)

    def get_prods(self):
        # get ids from cart
        product_ids = self.cart.keys()
        # use ids to lookup products in database model
        products = Product.objects.filter(id__in=product_ids)
        # return looked up products
        return products

    def get_quants(self):
        # convert quantities dictionary for template use
        return {str(key): value for key, value in self.cart.items()}

    def update(self, product_id, quantity):
        # Ensure that product_id is a string and quantity is an integer
        product_id = str(product_id)  # Make sure it's a string
        product_qty = int(quantity)  # Convert quantity to integer

        # Log the update process
        logger.debug(f"Updating cart: Product ID: {product_id}, Quantity: {product_qty}")

        # Update the cart dictionary with the new quantity
        self.cart[product_id] = product_qty
        self.session.modified = True  # Mark session as modified to save changes

    def delete(self, product):
        product_id = str(product.id)
        # delete from dictionary/cart
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

    def cart_total(self):
        # get product ids
        product_ids = self.cart.keys()
        # lookup those keys in our product database model
        products = Product.objects.filter(id__in=product_ids)
        # get quantities
        quantities = self.cart
        # start counting at 0
        total = 0
        for product in products:
            product_id = str(product.id)
            total += product.price * int(quantities[product_id])

        return total
