document.addEventListener('DOMContentLoaded', function () {
    // Filter function
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

    // Toggle wishlist button color on click
    document.querySelectorAll('.wishlist').forEach(button => {
        button.addEventListener('click', function () {
            button.classList.toggle('active');
        });
    });

    // Redirect to aboutus page on Add to Cart button click
    document.querySelectorAll('.RRcard .add-to-cart').forEach(button => {
        button.addEventListener('click', function () {
            window.location.href = aboutusUrl;
        });
    });
});
