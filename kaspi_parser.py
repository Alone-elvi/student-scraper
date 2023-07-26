import bs4
import requests

from icecream import ic

PARSING_MAIN_URL = "https://kaspi.kz/"

PARSING_URL = "https://kaspi.kz/shop/c/notebooks%20and%20accessories/"

PARSING_CATEGORITES = "?q=%3AavailableInZones%3AMagnum_ZONE1%3Acategory%3ANotebooks%20and%20accessories%3AmanufacturerName%3AASUS&sort=relevance&sc="
PARSING_SHOP = "shop/p/"

USER_AGENT = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15"
}

HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "User-Agent": USER_AGENT["User-Agent"],
}


def get_page(url):
    ses = requests.Session()
    response = ses.get(url=url, headers=HEADERS)

    with open("page.html", "w", encoding="utf-8") as file:
        file.write(response.text)
    
    return response


def get_soup(url: str) -> bs4.BeautifulSoup:
    result = requests.get(url, headers=USER_AGENT)
    return bs4.BeautifulSoup(result.text, "html.parser")


def get_items(soup: bs4.BeautifulSoup) -> bs4.BeautifulSoup:
    return soup


def get_categories() -> bs4.BeautifulSoup:
    category_page = get_soup(PARSING_URL + PARSING_CATEGORITES)
    return category_page.findAll(
        "div", class_="item-card ddl_product ddl_product_link undefined"
    )


def get_data():
    for item in get_categories():
        item = get_soup(item.a["href"])
        ic(item)
    return get_soup()


def main():
    get_page(url=PARSING_URL)


if __name__ == "__main__":
    main()
