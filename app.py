from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
import sqlite3

app = Flask(__name__)


# Endpoint to register a page visit and collect data on it
@app.route('/register_page_visit', methods=['POST'])
def register_page_visit():
    # Retrieve URL from the POST request
    url = request.json['url']

    # Make a request to the URL and retrieve its status code
    response = requests.get(url)
    status_code = response.status_code

    # If there is a redirect, get the final URL and final status code
    if response.history:
        final_url = response.url
        final_status_code = response.history[0].status_code
    else:
        final_url = ""
        final_status_code = None

    # Parse the page's HTML and retrieve its title
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.title.string.strip() if soup.title else ""

    # Get the domain name of the site
    domain_name = url.split('/')[2]

    # Save the data to the SQLite database
    conn = sqlite3.connect('pages.db')
    cursor = conn.cursor()
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS page_visits
            (url TEXT, final_url TEXT, status_code INT, final_status_code INT, title TEXT, domain_name TEXT)''')
    cursor.execute('INSERT INTO page_visits VALUES (?, ?, ?, ?, ?, ?)', (url, final_url, status_code, final_status_code,
                                                                         title, domain_name))
    conn.commit()
    conn.close()

    # Return the saved data in JSON format
    data = {
        'final_url': final_url,
        'final_status_code': final_status_code,
        'status_code': status_code,
        'title': title,
        'domain_name': domain_name
    }
    return jsonify(data)


# Endpoint to obtain statistics by domain
@app.route('/get_domain_statistics', methods=['POST'])
def get_domain_statistics():
    # Retrieve domain name from the POST request
    domain_name = request.json['domain_name']

    # Retrieve data from the SQLite database
    conn = sqlite3.connect('pages.db')
    cursor = conn.cursor()

    # Query the database for number of active urls and total urls visited for the given domain
    cursor.execute("SELECT COUNT(*) FROM page_visits WHERE domain_name = ?", (domain_name,))
    total_page_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM page_visits WHERE domain_name = ? AND status_code = 200", (domain_name,))
    active_page_count = cursor.fetchone()[0]

    # Query the database for list of urls for the given domain
    cursor.execute("SELECT url FROM page_visits WHERE domain_name = ?", (domain_name,))
    url_list = [row[0] for row in cursor.fetchall()]

    # Close database connection
    cursor.close()
    conn.close()

    # Return statistics as json response
    response_data = {
        'active_page_count': active_page_count,
        'total_page_count': total_page_count,
        'url_list': url_list
    }
    return jsonify(response_data)


if __name__ == '__main__':
    app.run(debug=False)
