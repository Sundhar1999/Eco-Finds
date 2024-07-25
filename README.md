# Eco-Finds 🌿


## Overview

**Eco-Finds** is an innovative e-commerce platform that promotes sustainable living by providing a wide range of eco-friendly products. Our mission is to make eco-friendly shopping easy, enjoyable, and accessible. 

## Key Features

- **🌱 Eco-Friendly Products**: A curated selection of products that are sustainable and environmentally friendly.
- **🎁 Rewards System**: Earn points for every purchase which can be redeemed for discounts on future purchases.
- **📝 Wishlist Functionality**: Save your favorite products to purchase later.
- **♻️ Environmental Impact Information**: Detailed CO2 emission data and environmental impact information for each product.
- **🔍 User-Centric Design**: A seamless, intuitive shopping experience with easy navigation and user-friendly interface.

## Technologies Used

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

## Project Structure

- **Home**: The main landing page with an overview of the platform.
- **Products**: A diverse range of eco-friendly products categorized for easy navigation.
- **Cart**: A dynamic shopping cart with real-time updates for product quantities, prices, and reward points.
- **Profile**: User account page with order history, wishlist, and profile details.
- **Wishlist**: A favourites page where users can add and save the products for future purchase.
- **Checkout**: Seamless checkout process with various payment options and address management.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/eco-finds.git
    cd eco-finds
    ```

2. Set up a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the migrations:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

6. Start the development server:
    ```bash
    python manage.py runserver
    ```

7. Access the application at `http://127.0.0.1:8000/`.

## Usage

- **User Registration**: Sign up to start shopping.
- **Browse Products**: Explore the wide range of eco-friendly products.
- **Add to Cart**: Add products to your shopping cart.
- **Wishlist**: Save your favorite products to the wishlist.
- **Checkout**: Complete your purchase with easy checkout options.
- **Earn Rewards**: Gain points with every purchase that can be redeemed for discounts.

## Contributing

We welcome contributions from the community. To contribute:

1. Fork the repository.
2. Create a new branch for your feature:
    ```bash
    git checkout -b feature-name
    ```
3. Commit your changes:
    ```bash
    git commit -m "Add a new feature"
    ```
4. Push to the branch:
    ```bash
    git push origin feature-name
    ```
5. Open a Pull Request.

