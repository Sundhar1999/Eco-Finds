document.addEventListener('DOMContentLoaded', () => {
    // Handle quantity increase and decrease
    document.querySelectorAll('.plus-btn, .minus-btn').forEach(button => {
        button.addEventListener('click', () => {
            const input = button.classList.contains('plus-btn') ? button.previousElementSibling : button.nextElementSibling;
            const url = button.getAttribute('data-url');
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    input.value = data.new_quantity;
                    updateTotalPrice(button.closest('tr'), data.new_total_price);
                } else {
                    alert('Failed to update item quantity.');
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });

    // Handle delete button
    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', () => {
            const row = button.closest('tr');
            const url = button.getAttribute('data-url');
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    row.remove();
                    updateCartTotal();
                } else {
                    alert('Failed to remove item from cart.');
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });

    // Handle wishlist button
    document.querySelectorAll('.wishlist-btn').forEach(button => {
        button.addEventListener('click', () => {
            const row = button.closest('tr');
            moveToWishlist(row);
            row.remove();
            updateCartTotal();
        });
    });

    // Function to update the total price for a single item
    function updateTotalPrice(row, newTotalPrice) {
        const totalPriceElement = row.querySelector('.total-price');
        totalPriceElement.textContent = `$${newTotalPrice.toFixed(2)}`;
        updateCartTotal();
    }

    // Function to calculate the tax for a single item based on its category
    function calculateTax(row) {
        const category = row.getAttribute('data-product-category');
        const price = parseFloat(row.querySelector('.total-price').textContent.replace('$', ''));
        let taxRate = 0;

        switch (category) {
            case 'Recycled Products':
                taxRate = 0.12;
                break;
            case 'Men Clothing':
                taxRate = 0.15;
                break;
            case 'Women Clothing':
                taxRate = 0.12;
                break;
            case 'Home Essentials':
                taxRate = 0.22;
                break;
            case 'Summer Collection':
                taxRate = 0.16;
                break;
            case 'Kids Section':
                taxRate = 0.14;
                break;
            default:
                taxRate = 0.08;
                break;
        }

        return price * taxRate;
    }

    // Function to update the cart total and tax
    function updateCartTotal() {
        let total = 0;
        let totalTax = 0;
        document.querySelectorAll('.total-price').forEach(priceElement => {
            const row = priceElement.closest('tr');
            total += parseFloat(priceElement.textContent.replace('$', ''));
            totalTax += calculateTax(row);
        });
        document.querySelector('.cart-footer .total p span.cart-total').textContent = total.toFixed(2);
        document.querySelector('.cart-footer .total p span.cart-tax').textContent = totalTax.toFixed(2);
    }

    // Function to move an item to the wishlist
    function moveToWishlist(row) {
        const productId = row.dataset.productId;
        fetch(`/add_to_wishlist/${productId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify({ product_id: productId })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Item moved to wishlist!');
            } else {
                alert('Failed to move item to wishlist.');
            }
        })
        .catch(error => console.error('Error:', error));
    }

    // Function to get the CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Initial call to update cart total on page load
    updateCartTotal();

    // Re-apply styles on modal close
    window.addEventListener('resize', () => {
        document.querySelectorAll('.product img').forEach(img => {
            img.style.width = '100px';
            img.style.height = 'auto';
        });
    });

    document.getElementById('wishlistModal').addEventListener('click', (event) => {
        if (event.target.classList.contains('close-wishlist')) {
            document.querySelectorAll('.product img').forEach(img => {
                img.style.width = '100px';
                img.style.height = 'auto';
            });
        }
    });
});
