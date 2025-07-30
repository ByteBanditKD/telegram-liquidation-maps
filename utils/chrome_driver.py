from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def setup_chrome_driver():
    """
    Set up and configure Chrome driver for headless execution in Docker environment
    """
    chrome_options = webdriver.ChromeOptions()
    
    # Add necessary arguments for running in Docker
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-software-rasterizer')
    
    # Set window size for consistent screenshots
    chrome_options.add_argument('--window-size=1920,1080')
    
    # Set Chrome binary location
    chrome_options.binary_location = '/usr/bin/chromium'
    
    # Initialize Chrome driver with service
    service = Service(executable_path='/usr/bin/chromedriver')
    driver = webdriver.Chrome(
        service=service,
        options=chrome_options
    )
    
    return driver
