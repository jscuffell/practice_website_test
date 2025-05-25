from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import difflib

def get_gp_website(practice_name, postcode):
    print(practice_name)
    url = "https://www.nhs.uk/service-search/find-a-gp"

    # Set up headless browser
    options = webdriver.ChromeOptions()
#    options.add_argument('--headless')
#    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    try:
        driver.get(url)
        time.sleep(3)

        # Input postcode or practice name
        # Step 2: Enter postcode
        postcode_input = driver.find_element(By.ID, "Location")
        postcode_input.clear()
        postcode_input.send_keys(postcode)  # Example postcode
        time.sleep(1)
        search_button = driver.find_element(By.XPATH, "//button[text()='Search']")
        search_button.click()
        time.sleep(3)

        # Collect all GP names and links
        links = driver.find_elements(By.CSS_SELECTOR, "h2.results__name a")

        best_match = None
        best_score = 0

        for link in links:
            name = link.text.strip()
            score = difflib.SequenceMatcher(None, name.lower(),
            practice_name.lower()).ratio()
            if score > best_score:
                best_score = score
                best_match = link

        # Click the best match
        if best_match:
            print("Clicking:", best_match.text)
            best_match.click()
            time.sleep(2)
            print("Now on page:", driver.current_url)
        else:
            print("No close match found.")
        time.sleep(3)
        link = driver.find_element(By.ID, "nav-link-contact-and-opening")
        print("Clicking link to:", link.get_attribute("href"))
        link.click()
        time.sleep(3)

        link = driver.find_element(By.ID, "contact_info_panel_website_link")
        print("Clicking link to:", link.get_attribute("href"))
        href = link.get_attribute("href")
        link.click()
        time.sleep(3)
        
        return href

    finally:
        driver.quit()

# Example usage:
#url = get_gp_website("THE PARK PRACTICE", "SE20 8QA")
#print("Website URL:", url)



import pandas as pd
import random

def run_batch_from_epraccur():
    df = pd.read_csv("epraccur.csv", header=None)
    df = df[[1, 9]]  # practice_name, postcode
    df.columns = ["practice_name", "postcode"]
    df = df.dropna()

    sample = df.sample(n=5, random_state=42)

    for _, row in sample.iterrows():
        name = row["practice_name"]
        postcode = row["postcode"]
        try:
            url = get_gp_website(name, postcode)
        except Exception as e:
            url = f"ERROR: {e}"
        print(f"{name},{postcode},{url}")

if __name__ == "__main__":
    run_batch_from_epraccur()
