// $('.like-btn').on('click', function() {
//     $(this).toggleClass('is-active');
// });
//
// $('.minus-btn').on('click', function(e) {
//     e.preventDefault();
//     var $this = $(this);
//     var $input = $this.closest('div').find('input');
//     var value = parseInt($input.val());
//
//     if (value > 1) {
//         value = value - 1;
//     } else {
//         value = 0;
//     }
//
//     $input.val(value);
// });
//
// $('.plus-btn').on('click', function(e) {
//     e.preventDefault();
//     var $this = $(this);
//     var $input = $this.closest('div').find('input');
//     var value = parseInt($input.val());
//
//     if (value < 100) {
//         value = value + 1;
//     } else {
//         value = 100;
//     }
//
//     $input.val(value);
// });
// document.addEventListener('DOMContentLoaded', () => {
//     // Handle quantity increase and decrease
//     document.querySelectorAll('.plus-btn').forEach(button => {
//         button.addEventListener('click', () => {
//             const input = button.previousElementSibling;
//             input.value = parseInt(input.value) + 1;
//             updateTotalPrice(button.closest('tr'));
//         });
//     });
//
//     document.querySelectorAll('.minus-btn').forEach(button => {
//         button.addEventListener('click', () => {
//             const input = button.nextElementSibling;
//             if (parseInt(input.value) > 1) {
//                 input.value = parseInt(input.value) - 1;
//                 updateTotalPrice(button.closest('tr'));
//             }
//         });
//     });
//
//     // Handle delete button
//     document.querySelectorAll('.delete-btn').forEach(button => {
//         button.addEventListener('click', () => {
//             const row = button.closest('tr');
//             row.remove();
//             updateCartTotal();
//         });
//     });
//
//     // Handle favorite button (heart)
//     document.querySelectorAll('.heart-btn').forEach(button => {
//         button.addEventListener('click', () => {
//             button.classList.toggle('favorite');
//         });
//     });
//
//     // Function to update the total price for a single item
//     function updateTotalPrice(row) {
//         const priceElement = row.querySelector('td:nth-child(2)');
//         const price = parseFloat(priceElement.textContent.replace('$', ''));
//         const quantity = parseInt(row.querySelector('.quantity input').value);
//         const totalPriceElement = row.querySelector('.total-price');
//         totalPriceElement.textContent = `$${(price * quantity).toFixed(2)}`;
//         updateCartTotal();
//     }
//
//     // Function to update the cart total
//     function updateCartTotal() {
//         let total = 0;
//         document.querySelectorAll('.total-price').forEach(priceElement => {
//             total += parseFloat(priceElement.textContent.replace('$', ''));
//         });
//         document.querySelector('.cart-footer .total p:nth-child(2)').textContent = `Total: $${total.toFixed(2)}`;
//     }
// });
//
// // Wishlist operations <-> Cart
// document.addEventListener('DOMContentLoaded', () => {
//     // Handle quantity increase and decrease
//     document.querySelectorAll('.plus-btn').forEach(button => {
//         button.addEventListener('click', () => {
//             const input = button.previousElementSibling;
//             input.value = parseInt(input.value) + 1;
//             updateTotalPrice(button.closest('tr'));
//         });
//     });
//
//     document.querySelectorAll('.minus-btn').forEach(button => {
//         button.addEventListener('click', () => {
//             const input = button.nextElementSibling;
//             if (parseInt(input.value) > 1) {
//                 input.value = parseInt(input.value) - 1;
//                 updateTotalPrice(button.closest('tr'));
//             }
//         });
//     });
//
//     // Handle delete button
//     document.querySelectorAll('.delete-btn').forEach(button => {
//         button.addEventListener('click', () => {
//             const row = button.closest('tr');
//             row.remove();
//             updateCartTotal();
//         });
//     });
//
//     // Handle wishlist button
//     document.querySelectorAll('.wishlist-btn').forEach(button => {
//         button.addEventListener('click', () => {
//             const row = button.closest('tr');
//             moveToWishlist(row);
//             row.remove();
//             updateCartTotal();
//         });
//     });
//
//     // Function to update the total price for a single item
//     function updateTotalPrice(row) {
//         const priceElement = row.querySelector('td:nth-child(2)');
//         const price = parseFloat(priceElement.textContent.replace('$', ''));
//         const quantity = parseInt(row.querySelector('.quantity input').value);
//         const totalPriceElement = row.querySelector('.total-price');
//         totalPriceElement.textContent = `$${(price * quantity).toFixed(2)}`;
//         updateCartTotal();
//     }
//
//     // Function to update the cart total
//     function updateCartTotal() {
//         let total = 0;
//         document.querySelectorAll('.total-price').forEach(priceElement => {
//             total += parseFloat(priceElement.textContent.replace('$', ''));
//         });
//         document.querySelector('.cart-footer .total p:nth-child(2)').textContent = `Total: $${total.toFixed(2)}`;
//     }
//
//     // Function to move an item to the wishlist
//     function moveToWishlist(row) {
//         // Add the functionality to move the item to the wishlist
//         alert('Item moved to wishlist!');
//     }
// });

document.addEventListener('DOMContentLoaded', () => {
    // Handle quantity increase and decrease
    document.querySelectorAll('.plus-btn').forEach(button => {
        button.addEventListener('click', () => {
            const input = button.previousElementSibling;
            input.value = parseInt(input.value) + 1;
            updateTotalPrice(button.closest('tr'));
        });
    });

    document.querySelectorAll('.minus-btn').forEach(button => {
        button.addEventListener('click', () => {
            const input = button.nextElementSibling;
            if (parseInt(input.value) > 1) {
                input.value = parseInt(input.value) - 1;
                updateTotalPrice(button.closest('tr'));
            }
        });
    });

    // Handle delete button
    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', () => {
            const row = button.closest('tr');
            row.remove();
            updateCartTotal();
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
    function updateTotalPrice(row) {
        const priceElement = row.querySelector('td:nth-child(2)');
        const price = parseFloat(priceElement.textContent.replace('$', ''));
        const quantity = parseInt(row.querySelector('.quantity input').value);
        const totalPriceElement = row.querySelector('.total-price');
        totalPriceElement.textContent = `$${(price * quantity).toFixed(2)}`;
        updateCartTotal();
    }

    // Function to update the cart total
    function updateCartTotal() {
        let total = 0;
        document.querySelectorAll('.total-price').forEach(priceElement => {
            total += parseFloat(priceElement.textContent.replace('$', ''));
        });
        document.querySelector('.cart-footer .total p:nth-child(2)').textContent = `Total: $${total.toFixed(2)}`;
    }

    // Function to move an item to the wishlist
    function moveToWishlist(row) {
        const productId = row.dataset.productId;  // Assumes there's a data-product-id attribute in the row
        fetch(`/add_to_wishlist/${productId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')  // Assumes a function to get the CSRF token
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
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
