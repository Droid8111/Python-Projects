from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image
import pytesseract
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.amazon.ca/KOORUI-Ultrawide-Curved-Gaming-Monitor/dp/B0C4P2KB9K")

def extract_price():
    try:
        price_element = driver.find_element(By.CLASS_NAME, "a-price-whole")
        return price_element.text
    except Exception as e:
        print(f"Price not found")
        return None

while True:
    price = extract_price()
    if price:
        print(f"Price found: {price}")
        break
    
    driver.save_screenshot("screenshot.png")

    # Open the screenshot image
    screenshot = Image.open("screenshot.png")
    
    # Define path to tesseract.exe
    path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    
    # Provide the tesseract executable location to pytesseract library
    pytesseract.pytesseract.tesseract_cmd = path_to_tesseract
    
    # Extract text from the screenshot
    full_text = pytesseract.image_to_string(screenshot)

    # Extract the desired text
    start_phrase = "this image:\n"
    end_phrase = "Try different image"
    start_index = full_text.find(start_phrase) + len(start_phrase)
    end_index = full_text.find(end_phrase)
    desired_text = full_text[start_index:end_index].strip()

    print(f"Extracted text: {desired_text}")

    input_field = driver.find_element(By.NAME, "field-keywords")
    input_field.clear()
    input_field.send_keys(desired_text)

    search_button = driver.find_element(By.CLASS_NAME, "a-button-text")
    search_button.click()

    time.sleep(5)  # Adjust sleep time as needed

driver.quit()
