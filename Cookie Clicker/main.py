from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import keyboard
import random

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://orteil.dashnet.org/cookieclicker/")

time.sleep(5)

is_paused = False

def toggle_pause():
    global is_paused
    is_paused = not is_paused

def stop_loop():
    global loop
    loop = False

# Listen for the 'p' key to toggle the pause state
keyboard.add_hotkey('p', toggle_pause)
keyboard.add_hotkey('q', stop_loop)

def beginning_lang():
    try:
        lang = driver.find_element(By.ID, "langSelect-EN")
        lang.click()
    except Exception as e:
        print(f"Exception in beginning_lang: {e}")
        return None

def get_product_price(product_price):
    price_text = product_price.text.strip().replace(',', '')
    parts = price_text.split(' ')
    
    if len(parts) == 1:
        return float(parts[0]) if parts[0].isdigit() else None
    elif len(parts) == 2:
        number = float(parts[0])
        unit = parts[1].lower()
        if unit == "million":
            return int(number * 1_000_000)
        elif unit == "billion":
            return int(number * 1_000_000_000)
        else:
            return None
    else:
        return None


def check_upgrade(cookie_count):
    product_prices = []
    for i in range(20):  # Assuming you have 20 products
        product_price_id = f"productPrice{i}"
        try:
            product_price_element = driver.find_element(By.ID, product_price_id)
            price = get_product_price(product_price_element)
            if price is not None:
                #parent_element = product_price_element.find_element(By.XPATH, "./..")  # Find parent element correctly
                parent_element = driver.find_element(By.ID, f"product{i}")
                product_prices.append((parent_element, price))
        except Exception as e:
            print(f"Exception while fetching product {product_price_id}: {e}")
            continue
    
    # Sort the products by price in descending order
    product_prices.sort(key=lambda x: x[1], reverse=True)

    for parent_element, price in product_prices:
        print(f"Product: {parent_element.get_attribute('id')}, Price: {price}")  # Debugging line
    
    for parent_element, price in product_prices:
        if price < (cookie_count*2):
            try:
                # Use WebDriverWait to wait until element is clickable
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, parent_element.get_attribute("id"))))
                parent_element.click()
                print(f"Clicked on product with price {price}")
                break  # Exit the loop after clicking the highest affordable product
            except Exception as e:
                print(f"Exception in clicking: {e}")
                continue

def close_notification():
    try:
        notification = driver.find_element(By.CLASS_NAME, "close")
        notification.click()
        print("Closed notification")
    except Exception:
        return None
    else:
        close_notification()

def get_upgrade():
    try:
        print("Trying to get upgrade")
        upgrade = driver.find_element(By.ID, "upgrade0")
        upgrade.click()
    except Exception:
        print("Failed to get upgrade")
        return None

def get_golden_cookie():
    try:
        golden_cookie = driver.find_element(By.ID, "shimmers")
        golden_cookie.click()
    except Exception:
        return None
    
def bulk_buy(cookie_count):
    bulk_buy = driver.find_element(By.ID, "storeBulk10")
    bulk_buy.click()
    check_upgrade(cookie_count) 
    normal_buy = driver.find_element(By.ID, "storeBulk1")
    normal_buy.click()
    
def get_cookie_count(cookie_count_text):
    # Remove commas and split the text to handle units
    parts = cookie_count_text.replace(',', '').split(' ')
    
    # Default multiplier
    multiplier = 1
    
    # Check for units
    if len(parts) > 1:
        number = float(parts[0])
        unit = parts[1]
        if unit == "million":
            multiplier = 1000000
        elif unit == "billion":
            multiplier = 1000000000
    else:
        number = float(parts[0])
    
    return int(number * multiplier)


def extract_cookie_count(text):
    parts = text.split('\n')
    if len(parts) >= 2 and 'million' in parts[1]:
        return parts[0] + ' million'
    elif len(parts) >= 2 and 'billion' in parts[1]:
        return parts[0] + ' billion'
    else:
        return parts[0]

#################################   MAIN LOOP   #################################


beginning_lang()

time.sleep(5)
cookie = driver.find_element(By.ID, "bigCookie")
cookie_count_element = driver.find_element(By.ID, "cookies")

loop = True
while loop:
    if not is_paused:
        start_time = time.time()
        while time.time() - start_time < 5:
            cookie.click()
        
        raw_cookie_count_text = cookie_count_element.text
        print(f"Raw cookie count text: {raw_cookie_count_text}")  # Debugging line
        
        cookie_count_text = extract_cookie_count(raw_cookie_count_text)
        print(f"Extracted cookie count text: {cookie_count_text}")  # Debugging line
        cookie_count = get_cookie_count(cookie_count_text)
        
        print(f"Cookie count: {cookie_count}")  # Debugging line
        
        if random.randint(0, 19) == 0:  # 1% chance
            bulk_buy(cookie_count)
        
        get_upgrade()
        get_golden_cookie()
        cookie.click()
        check_upgrade(cookie_count)
        close_notification()

driver.quit()