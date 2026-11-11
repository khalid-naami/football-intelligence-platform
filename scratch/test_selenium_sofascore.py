from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

print("Launching Chrome via Selenium...")
try:
    driver = webdriver.Chrome(options=options)
    print("Navigating to https://www.sofascore.com/football ...")
    driver.get("https://www.sofascore.com/football")
    time.sleep(5)
    title = driver.title
    print("Page Title:", title)
    
    # Try finding live/match elements
    cards = driver.find_elements(By.CSS_SELECTOR, "[data-testid='event-list-item'], [data-id], a[href*='/match/']")
    print(f"Found {len(cards)} match elements!")
    
    # Check page source length
    src_len = len(driver.page_source)
    print(f"Page source length: {src_len} chars")
    
    driver.quit()
    print("Selenium test completed successfully!")
except Exception as e:
    print("Selenium error:", e)
