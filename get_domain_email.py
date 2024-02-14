from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time, random, re, csv

def scroll_down():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            try:
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="botstuff"]/div/div[3]/div[4]/a[1]/h3/div'))
                )
                element.click()
            except Exception:
                break
        last_height = new_height


def get_urls(min_da, max_da):
    urls = []
    serp_listings = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "MjjYud"))
    )
    for listing in serp_listings:
        try:
            da_element = listing.find_element(By.XPATH, ".//div[contains(@class, 'ah_serpbar__item-inner')]/span[contains(@class, 'ah_serpbar__item-label') and text()='dr']/following-sibling::span[contains(@class, 'ah_serpbar__item-data')]")
            da_number = float(da_element.text)
            
            if min_da <= da_number <= max_da:
                listing_link = listing.find_element(By.TAG_NAME, 'a').get_attribute('href')
                print(f"Domain Authority: {da_number} Link: {listing_link}")
                urls.append(listing_link)
        except Exception as e:
            print(e)
            continue
    return urls

if (__name__ == '__main__'):

    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-geolocation")
    chrome_options.add_argument("--remote-allow-origins=*")
    chrome_options.add_argument('user-data-dir=/Users/williamzhao/Library/Application Support/Google/Chrome/')
    chrome_options.add_argument("--profile-directory=Profile 1")
    chrome_options.add_argument("--start-maximized")
    service = Service(executable_path='/opt/homebrew/bin/chromedriver')

    driver = webdriver.Chrome(service=service, options=chrome_options)

    # d={}

    search_queries = [
    '"gym owners" + "business email" -site:facebook.com',
    '"personal trainer" + "contact" + email -site:instagram.com',
    '"fitness studio" + "email address" -site:twitter.com',
    '"health and wellness" + "business contact" -site:youtube.com',
    '"fitness professionals" + "email directory" -site:pinterest.com',
    '"gym contact information" + email -site:linkedin.com -site:facebook.com',
    '"fitness industry" + "staff emails" -site:instagram.com -site:twitter.com',
    '"fitness clubs" + "owner email" -site:youtube.com -site:pinterest.com',
    '"fitness workshops" + "email contact" -site:linkedin.com -site:facebook.com',
    '"boxing gym owner" + contact',
    '"aerobics instructor" + "email address"',
    '"fitness blogger" + "contact info"',
    '"strength and conditioning coach" + email',
    '"group fitness instructor" + "contact"',
    '"outdoor fitness" + "owner contact"',
    '"fitness app developer" + "business contact"',
    '"athletic trainer" + "contact information"',
    '"cycling instructor" + "business email"',
    '"fitness equipment supplier" + contact',
    '"sports therapist" + "business contact"',
    '"mobility coach" + "contact information"',
    '"fitness podcast host" + email',
    '"virtual fitness coach" + "contact info"',
    '"bodybuilding coach" + "business email"',
    '"swim coach" + "contact information"',
    '"fitness consultant" + "business contact"',
    '"nutrition consultant" + "email address"'
    ]


    with open("email_out/emails.csv", 'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerow(['emails'])

        for query in search_queries:
            time.sleep(random.randrange(1, 5))

            try:
                driver.get(f"https://www.google.com/search?q={query}")
                scroll_down()
                urls=get_urls(0, 61)

                for url in urls:
                    try:
                        driver.get(url)
                        domain = url.split("//")[-1].split("/")[0]
                        regex = r"[a-zA-Z0-9._%+-]+@" + re.escape(domain)
                        html = driver.page_source
                        emails = list(set(re.findall(regex, html)))
                        if (emails):writer.writerow(emails)
                    except Exception:
                        continue
            except Exception:
                continue


time.sleep(999)
driver.quit()