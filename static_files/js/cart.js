document.addEventListener('DOMContentLoaded', () => {
    // Update quantity
    document.querySelectorAll('.quantity-btn').forEach((btn) => {
        btn.addEventListener('click', function () {
            const action = this.dataset.action;
            const cartItemId = this.dataset.cartItemId;

            fetch(`/cart/update/${cartItemId}/${action}/`, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data.quantity === 0) {
                        document.querySelector(`#cart-item-${cartItemId}`).remove(); // Remove the row if quantity is zero
                    } else {
                        document.querySelector(`#quantity-${cartItemId}`).textContent = data.quantity;
                        document.querySelector(`#total-price-${cartItemId}`).textContent = `KSHS ${data.total_price}`;
                    }
                    // Update total price
                    document.querySelector('#cart-total').textContent = `Total: KSHS ${data.cart_total}`;
                })
                .catch((error) => console.error('Error:', error));
        });
    });

    // Remove item
    document.querySelectorAll('.remove-btn').forEach((btn) => {
        btn.addEventListener('click', function () {
            const cartItemId = this.dataset.cartItemId;

            fetch(`/cart/remove/${cartItemId}/`, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data.status === 'success') {
                        document.querySelector(`#cart-item-${cartItemId}`).remove();
                        // Optionally, recalculate and update the total
                        const newTotal = Array.from(document.querySelectorAll('.total-price'))
                            .reduce((sum, priceEl) => sum + parseFloat(priceEl.textContent.replace('KSHS ', '')), 0);
                        document.querySelector('#cart-total').textContent = `Total: KSHS ${newTotal}`;
                    }
                })
                .catch((error) => console.error('Error:', error));
        });
    });
});
