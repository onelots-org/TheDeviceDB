import cloudscraper
import bs4
import json
import time

scraper = cloudscraper.create_scraper()
url = "https://www.gsmarena.com/makers.php3"
browser = {
    "browser": "chrome",
    "platform": "windows",
    "mobile": False
}


def extract_brands():
    scraper = cloudscraper.create_scraper(browser=browser)
    result = scraper.get(url)
    soup = bs4.BeautifulSoup(result.text, "html.parser")
    brands = soup.findAll("td")
    brand_list = []
    for brand in brands:
        a = brand.find("a")
        if a:
            name = a.contents[0].strip()
            brand_list.append(name)

    with open("resources/vendors.json", "w") as f:
        json.dump(brand_list, f, indent=4)

    return brand_list


extract_brands()