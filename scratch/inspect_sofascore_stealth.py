from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.get("https://www.sofascore.com/football")
time.sleep(8)
print("Title:", driver.title)
html = driver.page_source
print("HTML snippet:", html[:500])
with open("scratch/sofascore_page.html", "w", encoding="utf-8") as f:
    f.write(html)
driver.quit()
print("Saved page to scratch/sofascore_page.html")
