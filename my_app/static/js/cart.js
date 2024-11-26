function updateCart(cartItemId, action) {
    fetch(`/update_cart_quantity/${cartItemId}/${action}/`, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
    })
    .then(response => response.json())
    .then(data => {
        location.reload();
    })
    .catch(error => console.error('Error:', error));
}
