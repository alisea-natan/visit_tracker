# Page Visit Tracker
This is a Python Flask web service that tracks page visits and collects information about them, implementing an API with 2 endpoints. The system uses SQLite as its database and is designed to handle large volumes of data.

## Getting Started
### Prerequisites
To run this application, you'll need to have the following software installed on your computer:
* Python 3.7+
* SQLite
### Installation
1. Clone the repository.
1. Create a virtual environment: python3 -m venv venv
1. Activate the virtual environment: source venv/bin/activate
1. Install the dependencies: pip install -r requirements.txt
1. Start the server: python app.py

## API Endpoints

### Registration of a Page Visit and Data Collection on it
**Endpoint:** /register_page_visit

**Method:** POST

**Input Parameter:**
*`url`: The URL of the page visited by the user.

**Output:**
* `final_url`: The final URL (if a redirect happened).
* `final_status_code`: The final status code (if a redirect happened).
* `status_code`: The status code of the initial URL.
* `title`: The title of the page.
* `domain_name`: The domain name of the site.

**Example Request:**

`{
    "url": "https://cyberchimps.com/blog/"
}`

**Example Response:**

`{
    "final_url": "",
    "final_status_code": null,
    "status_code": 200,
    "title": "Free & Premium WordPress Themes Blog, WP Themes",
    "domain_name": "cyberchimps.com"
}`

### Obtaining Statistics by Domain
**Endpoint:** /get_domain_stats

**Method:** POST

**Input Parameter:**

* `domain_name`: The domain name for which to obtain statistics.

**Output:**

* `active_page_count`: The total number of active URLs with status code 200.
* `total_page_count`: The total number of visited domain URLs.
* `url_list`: A list of all visited domain URLs.

**Example Request:**

`{
    "domain_name": "cyberchimps.com"
}`

**Example Response:**

`{
    "active_page_count": 3,
    "total_page_count": 4,
    "url_list": [
        "https://cyberchimps.com/blog/top-wordpress-photography-themes/",
        "https://cyberchimps.com/blog/best-wordpress-themes-for-artists/",
        "https://cyberchimps.com/blog/qweqweqwe/",
        "https://cyberchimps.com/blog/"
    ]
}`