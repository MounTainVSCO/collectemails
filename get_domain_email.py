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

    search_queries = [

    '"climbing coach"',
    '"skiing instructor"',
    '"snowboarding instructor"',
    '"surfing coach"',
    '"kettlebell training specialist"',
    '"mobility coach"',
    '"pre and postnatal fitness coach"',
    ]


    # Change the mode to 'a' for appending data to the existing CSV file.
    with open("email_out/emails.csv", 'a', newline="") as f:
        writer = csv.writer(f)

        for query in search_queries:
            driver.get(f"https://www.google.com/search?q={query}")
            scroll_down()
            try:
                
                urls = get_urls(15, 61)

                for url in urls:
                    try:
                        driver.get(url)
                        time.sleep(0.5)
                        domain = url.split("//")[-1].split("/")[0]
                        regex = r"[a-zA-Z0-9._%+-]+@" + re.escape(domain)
                        html = driver.page_source
                        emails = list(set(re.findall(regex, html)))
                        print(emails)
                        if emails:
                            # Open the CSV file in append mode here within the loop
                            with open("email_out/emails.csv", 'a', newline="") as f:
                                writer = csv.writer(f)
                                writer.writerow(emails)
                    except Exception:
                        continue
            except Exception:
                continue

    driver.quit()
