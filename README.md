# Amazon Crawler Project

This project is a web scraper built with Python and Flask that extracts product data from Amazon, stores it in a MySQL database, and allows you to search for products and view their details. The scraper uses BeautifulSoup for parsing HTML and handles multiple retries and proxy rotations to avoid getting blocked by Amazon.

## Features

- Scrape product details including name, price, description, and customer reviews from Amazon.
- Store scraped data in a MySQL database.
- Simple web interface for searching products.
- Rotates user agents and proxies to avoid getting blocked.

## Requirements

- Python 3.x
- Flask
- BeautifulSoup4
- Requests
- MySQL Connector/Python

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/amazon-crawler.git
    cd amazon-crawler
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up your MySQL database:**

    ```sql
    CREATE DATABASE product;
    ```

5. **Configure your database credentials in the code:**

    Update the following lines in the `search` function:

    ```python
    cnx = mysql.connector.connect(user='root',
                                  password='Your password',
                                  host='localhost',
                                  database='product')
    ```

6. **Run the Flask app:**

    ```bash
    python app.py
    ```

## Usage

1. **Open your browser and navigate to:**

    ```
    http://127.0.0.1:5000/
    ```

2. **Enter a product name in the search box and submit.**

3. **The application will scrape Amazon for the product details and store them in the MySQL database.**

## Code Overview

### `app.py`

- **Imports and Setup:**
    ```python
    from flask import Flask, render_template, request
    from bs4 import BeautifulSoup
    import requests
    import random
    import time
    import mysql.connector

    app = Flask(__name__)
    ```

- **Headers and Proxies:**
    - Lists of user-agent headers and proxies to avoid getting blocked by Amazon.

- **`scrape_amazon` Function:**
    - Scrapes product data from Amazon including name, price, description, and customer reviews.
    - Rotates user-agent headers and proxies.
    - Handles multiple retries and exceptions.

- **Routes:**
    - `/` : Renders the search form.
    - `/search` : Handles the search form submission, scrapes Amazon, stores data in MySQL, and displays the results.

### HTML Templates

- **`templates/index.html`**
    - Simple form for entering the product name.

## Database Schema

- **Table: `product_info`**
    - `id`: INT, Primary Key, Auto Increment
    - `product_description`: VARCHAR(500)
    - `price`: VARCHAR(25)
    - `category`: VARCHAR(500)
    - `customer_name`: VARCHAR(200)
    - `rating`: VARCHAR(500)
    - `comment`: VARCHAR(5000)

## Database Operations

You can use the following SQL commands to interact with the database:

- **Select the database:**
    ```sql
    USE product;
    ```

- **Show tables in the database:**
    ```sql
    SHOW TABLES;
    ```

- **Select all data from the `product_info` table:**
    ```sql
    SELECT * FROM product_info;
    ```

- **Drop the `product_info` table:**
    ```sql
    DROP TABLE product_info;
    ```

## Notes

- Make sure to update the `headers_list` and `proxies` with valid user-agent strings and proxy addresses.
- Be aware of Amazon's terms of service regarding web scraping.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Contact

For any questions or feedback, please contact [kushagrataneja2004@gmail.com](mailto:kushagrataneja2004@gmail.com).
