document.addEventListener('DOMContentLoaded', function () {
    const products = [
        { name: "Soap Bar", price: 10, imageUrl: "soap.jpg", rating: 4, category: "home", carbonEmission: "0.2kg CO2", environmentalImpact: "This product uses natural ingredients that minimize harm to the environment." },
        { name: "Water Bottle", price: 29.00, imageUrl: "Water_bt.png", rating: 4, category: "home", carbonEmission: "0.3kg CO2" },
        { name: "Moisturizer", price: 15.99, imageUrl: "Moisturizer.jpg", rating: 5, category: "home", carbonEmission: "0.1kg CO2" },
        { name: "Brush", price: 22.50, imageUrl: "Brush.jpg", rating: 4, category: "home", carbonEmission: "0.4kg CO2" },
        { name: "Candle", price: 8.99, imageUrl: "Candle.jpg", rating: 3, category: "home", carbonEmission: "0.5kg CO2" },
        { name: "Sanitizer", price: 18.95, imageUrl: "Sanitizer.jpg", rating: 4, category: "home", carbonEmission: "0.2kg CO2" },
        { name: "Spoons Set", price: 12.00, imageUrl: "Spoons.jpg", rating: 5, category: "home", carbonEmission: "0.3kg CO2" },
        { name: "Men's Shirt", price: 14.20, imageUrl: "Shirt.jpg", rating: 5, category: "men", carbonEmission: "0.2kg CO2" },
        { name: "Shoe", price: 9.30, imageUrl: "Shoe.jpg", rating: 4, category: "men", carbonEmission: "0.1kg CO2" },
        { name: "Men's T-shirt", price: 27.99, imageUrl: "Tshirt.jpg", rating: 5, category: "men", carbonEmission: "0.3kg CO2" },
        { name: "White Shirt", price: 19.95, imageUrl: "White_Shrt.jpeg", rating: 4, category: "men", carbonEmission: "0.4kg CO2" },
        { name: "Men's Shirt", price: 15.40, imageUrl: "Shirt.jpg", rating: 4, category: "tea", carbonEmission: "0.2kg CO2" },
        { name: "Women's Blazzer ", price: 13.85, imageUrl: "Black_blaz.jpeg", rating: 5, category: "women", carbonEmission: "0.1kg CO2" },
        { name: "Women Tees", price: 16.75, imageUrl: "Black_Tees.jpeg", rating: 5, category: "women", carbonEmission: "0.3kg CO2" },
        { name: "Women Green Top", price: 21.90, imageUrl: "Greentop.jpeg", rating: 4, category: "women", carbonEmission: "0.2kg CO2" },
        { name: "Women Shoes", price: 21.90, imageUrl: "shoe.jpeg", rating: 4, category: "women", carbonEmission: "0.2kg CO2" },
        { name: "White Top", price: 21.90, imageUrl: "Whitetop.jpeg", rating: 4, category: "women", carbonEmission: "0.2kg CO2" }
    ];

    const container = document.querySelector('.RRcontainer.RRcategory');
    products.forEach(product => {
        const cardHtml = `
            <div class="RRcard" data-category="${product.category}">
                <img src="${product.imageUrl}" alt="${product.name}" style="height:200px; width:100%; object-fit:cover;">
                
<!--                &lt;!&ndash; Wishlist button &ndash;&gt;-->
<!--                <button class="wishlist" aria-label="Add to wishlist">-->
<!--                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-heart">-->
<!--                        <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>-->
<!--                    </svg>-->
<!--                </button>-->
<!--                -->
                <div class="info">
                    <h3 class="name">${product.name}</h3>
                    <p class="price">$${product.price}</p>
                    <div class="additional-info">
                        <span class="carbon-emission">Carbon: ${product.carbonEmission}</span> |
                        <span class="environmental-impact" title="Click for more info">Environmental Impact</span>
                        <div class="impact-info hidden">${product.environmentalImpact || 'No data available'}</div>
                        <span class="quantity-info">QTY: <span class="quantity-value">${product.quantity || 'N/A'}</span>
                    </div>
                    
                    <button class="add-to-cart">Add to Cart</button>
                    
                </div>
            </div>
        `;
        container.innerHTML += cardHtml;
    });

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
