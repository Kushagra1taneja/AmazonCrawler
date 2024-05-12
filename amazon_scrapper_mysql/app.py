from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests
import random
import time
import mysql.connector

app = Flask(__name__)


headers_list = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    
]




proxies = [
    'http://proxy1.example.com:port',
    'http://proxy2.example.com:port',
    
]

def scrape_amazon(product):
    base_url = f'https://www.amazon.in/s?k={product}&ref=nb_sb_noss_2'
    max_retries = 3
    scraped_data = []
    products_scraped = 0

    for retry in range(max_retries):
        try:
            headers = {'User-Agent': random.choice(headers_list)}
            proxy = {'http': random.choice(proxies)} 
            response = requests.get(base_url, headers=headers, proxies=proxy, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            product_link_elements = soup.find_all('a', {'class': 'a-text-normal'})

            for product_link_element in product_link_elements:
                if products_scraped >= 8:
                    break

                product_link = product_link_element['href']
                product_url = f'https://www.amazon.in{product_link}'
                product_response = requests.get(product_url, headers=headers, proxies=proxy, timeout=10)
                product_response.raise_for_status()
                product_soup = BeautifulSoup(product_response.content, 'html.parser')
                product_name_element = product_soup.find('span', {'class': 'a-size-large product-title-word-break'})
                product_name = product_name_element.text.strip() if product_name_element else "Name not available"
                price_element = product_soup.find('span', {'class': 'a-price-whole'})
                price = price_element.text.strip() if price_element else "Price not available"
                try:
                    description_element = product_soup.find('span', {'class': 'a-list-item'})
                    description = description_element.text.strip() if description_element else "Description not available"
                except Exception as e:
                    print(f"Error occurred while retrieving description: {e}")
                    description = "Description not available"
                review_elements = product_soup.find_all('div', {'data-hook': 'review'})
                reviews = []
                for review in review_elements:
                    customer_name_element = review.find('span', {'class': 'a-profile-name'})
                    customer_name = customer_name_element.text.strip() if customer_name_element else "Customer name not available"
                    rating_element = review.find('i', {'data-hook': 'review-star-rating'})
                    rating = rating_element.text.strip() if rating_element else "Rating not available"
                    comment_element = review.find('span', {'data-hook': 'review-body'})
                    comment = comment_element.text.strip() if comment_element else "Comment not available"
                    reviews.append((product_name, price, description, customer_name, rating, comment))

                scraped_data.extend(reviews)
                products_scraped += 1

            next_page_link = soup.find('li', {'class': 'a-last'}).find('a')['href']
            if next_page_link:
                base_url = f'https://www.amazon.in{next_page_link}'
            else:
                break

        except requests.HTTPError as e:
            if response.status_code == 503 and retry < max_retries - 1:
                print(f"503 Error occurred. Retrying ({retry+1}/{max_retries})...")
                time.sleep(random.uniform(5, 10))
                continue
            else:
                print(f"Error occurred: {e}")
                break

        except Exception as e:
            print(f"Error occurred: {e}")
            break

    print("Website successfully scraped")
    return scraped_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    product = request.form['product']
    scraped_data = scrape_amazon(product)
    print("List of Tuples:")
    for review_tuple in scraped_data:
        print(review_tuple)
    
   


    cnx = mysql.connector.connect(user='root',
                                  password='Kushagra01#',
                                  host='localhost',
                                  database='product')
    cursor = cnx.cursor()

    table_name = "prod"


    query = f"""
    CREATE TABLE {table_name} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        product_description varchar(500),
        price varchar(25),
        category varchar(500),
        custumer_name varchar(200),
        rating varchar(500),
        comment varchar(5000)
    )
    """
    cursor.execute(query)
    cnx.commit()





    insert_query = f"""
    INSERT INTO {table_name} (product_description, price, category,custumer_name, rating,comment) VALUES (%s, %s, %s, %s,%s,%s)
    """

    
    cursor.executemany(insert_query,scraped_data)

    cnx.commit()


    select_query = f"""
    SELECT * FROM {table_name}
    """
 
    cursor.execute(select_query)

    
    print("Values in the table:")
    for row in cursor.fetchall():
        print(row)


    cursor.close()
    cnx.close()
    return "Data scraped successfully"

if __name__ == '__main__':
    app.run(debug=True)
