from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-sync")

# Initialize driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

def exporta(url, find_by, name):
    driver.get(url)
    time.sleep(5)  # aguarda carregamento
    button_export = driver.find_element(find_by, name)
    button_export.click()
    time.sleep(2)

def exporta_fiis(url):
    driver.get(url)
    wait = WebDriverWait(driver, 30)  # Increased timeout

    try:
        # Wait for the page to stabilize
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # Check for iframes
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        if iframes:
            print(f"Found {len(iframes)} iframes, switching to the first one")
            driver.switch_to.frame(iframes[0])

        # Wait for the button's parent container
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.ml-auto")))

        # Locate the button using a more robust selector
        button_export = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Exportar lista completa de fundos"]')))

        # Scroll to the button
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button_export)
        time.sleep(1)

        # Click using JavaScript
        driver.execute_script("arguments[0].click();", button_export)
        print("Button clicked successfully")
        time.sleep(3)  # Wait for download to start

        # Switch back to main content if iframe was used
        driver.switch_to.default_content()

    except Exception as e:
        print(f"Error: {e}")
        # Save screenshot and page source for debugging
        driver.save_screenshot("error_screenshot.png")
        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

# URL
url_fiis = "https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/renda-variavel/fundos-de-investimentos/fii/fiis-listados/"
url_acoes = "https://www.dadosdemercado.com.br/acoes"

# Execute
exporta(url_acoes, By.ID, "download-csv")  # Ações
exporta_fiis(url_fiis) #FIIs

# Clean up
driver.quit()