import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# auto-close solution
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# selenium integration
url = "http://orteil.dashnet.org/experiments/cookie/"

driver = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))
driver.get(url)

# Get cookie to click on.
cookie = driver.find_element(By.ID, "cookie")

# Get upgrade item ids.
items = driver.find_elements(By.CSS_SELECTOR, "#store div")
item_ids = [item.get_attribute("id") for item in items]

timeout = time.time() + 5
five_min = time.time() + 300  # 5 minutes

all_items = driver.find_elements(By.CSS_SELECTOR, "#store b")

while True:
    cookie.click()

    # Every 5 seconds
    if time.time() > timeout:

        element_items = driver.find_elements(By.CSS_SELECTOR, "#store b")
        prices_items = []

        # Convert <b> text into an integer price.
        for price in element_items:
            price_text = price.text
            if price_text != "":
                cost = int(price_text.split("-")[1].strip().replace(",", ""))
                prices_items.append(cost)

        # Create dictionary of store items and prices
        cookie_upgrades = {}
        for n in range(len(prices_items)):
            cookie_upgrades[prices_items[n]] = item_ids[n]

        # Get current cookie count
        element_money = driver.find_element(By.ID, "money").text
        if "," in element_money:
            money_element = element_money.replace(",", "")
        cookie_count = int(element_money)

        # Find upgrades that we can currently afford
        affordable_upgrades = {}
        for cost, id in cookie_upgrades.items():
            if cookie_count > cost:
                affordable_upgrades[cost] = id

        # Purchase the most expensive affordable upgrade
        highest_price_affordable_upgrade = max(affordable_upgrades)
        print(highest_price_affordable_upgrade)
        to_purchase_id = affordable_upgrades[highest_price_affordable_upgrade]

        driver.find_element(By.ID, to_purchase_id).click()

        # Add another 5 seconds until the next check
        timeout = time.time() + 5

    # After 5 minutes stop the bot and check the cookies per second count.
    if time.time() > five_min:
        cookie_per_s = driver.find_element(By.ID, "cps").text
        print(cookie_per_s)
        break
