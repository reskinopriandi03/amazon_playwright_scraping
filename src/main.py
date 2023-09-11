#how to scrape using playwright to load page and send back the html then parse with selectolax/beautifulsoup, litle bit late for working just to know how to use and learn about it. the code read the existing csv, then we fill asin in csv and then show in terminal


from dataclasses import dataclass
from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
from rich import print
import csv

@dataclass
class Item:
    asin: str
    title: str
    price: str


def get_html(page, asin):
    url =f"https://www.amazon.co.uk/dp/{asin}" #Kode "dp" adalah bagian dari URL yang mengacu pada halaman produk di situs web Amazon. Kata "dp" singkatan dari "detail page," yang merupakan halaman spesifik yang menampilkan informasi tentang produk tertentu.
    page.goto(url)
    html = HTMLParser(page.content())
    return html

def parse_html(html, asin):
    item = Item(
        asin=asin,
        title=html.css_first("span#productTitle").text(strip=True),
        price=html.css_first("span.a-offscreen").text(strip=True)
    )
    return item

    #to check in terminal
    #print(html.css_first("title").text())
    #print(asin)

def read_csv():
    csv_path = 'product.csv'
    with open('product.csv', 'r') as f:
        reader = csv.reader(f)
        return [item[0] for item in reader]

def run(asin):
    #asin = "B0BSNSQBJ9"
    pw = sync_playwright().start()
    browser = pw.chromium.launch()
    page = browser.new_page()
    html = get_html(page, asin)
    product = parse_html(html, asin)
    print(product)
    # Menulis data ke dalam berkas CSV
   
    browser.close()
    pw.stop()

def main():
    asins = read_csv()
    for asin in asins:
        run(asin)
    #print(asins)
    #run()

if __name__ == "__main__":
    main()