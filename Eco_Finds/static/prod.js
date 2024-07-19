document.addEventListener('DOMContentLoaded', function () {
    function RRfilterProducts() {
        const selectedCategory = document.getElementById('RRcategorySelect').value;
        const cards = document.querySelectorAll('.RRcard');
        cards.forEach(card => {
            if (selectedCategory === 'all' || card.getAttribute('data-category') === selectedCategory) {
                card.style.display = '';
            } else {
                card.style.display = 'none';
            }
        });
    }

    document.getElementById('RRcategorySelect').addEventListener('change', RRfilterProducts);
    RRfilterProducts();

    document.querySelectorAll('.wishlist').forEach(button => {
        button.addEventListener('click', function () {
            button.classList.toggle('active');
        });
    });

    document.querySelectorAll('.add-to-cart-form').forEach(form => {
        form.addEventListener('submit', function (event) {
            event.preventDefault();
            const productId = form.action.split('/').pop();
            fetch(form.action, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({})
            }).then(response => {
                if (response.ok) {
                    response.json().then(data => {
                        if (data.success) {
                            const quantityInfo = form.closest('.RRcard').querySelector('.quantity-info');
                            quantityInfo.textContent = `QTY: ${data.new_quantity}`;
                            if (data.new_quantity === 0) {
                                form.outerHTML = '<p class="out-of-stock">Out of Stock</p>';
                            }
                        } else {
                            alert(data.message);
                        }
                    });
                }
            });
        });
    });
});
