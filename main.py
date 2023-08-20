import os, sys, logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def main():
    driver = openChrome()

    input("Press any key to exit...")
    driver.quit()

def openChrome(): # Start chrome browser and open WhatsApp Web
    # Get username of current active user
    user = os.environ["USERNAME"]

    # Setup Chrome driver options
    options = webdriver.ChromeOptions()

    # Setup download preference and user profile to save login state
    options.add_experimental_option("prefs", {
        "download.default_directory": os.path.join(os.getcwd(), "downloads"),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True})
    options.add_argument("--remote-debugging-port=9222")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument(
        "user-data-dir=C:\\Users\\" + user + "\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1")
    
    # Initialize browser
    driver = webdriver.Chrome(options=options)

    driver.get("http://web.whatsapp.com")
    
    # Check if WhatsApp Web login is successfull
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*/header/div[1]/div/img')))
        log.info("Connected to WhatsApp Web")
    except TimeoutException or NoSuchElementException:
        log.critical("Unable to connect to WhatsApp Web. Exiting...")
        driver.quit()
        sys.exit()

    return driver

def logger(): # Setup logging configuration
    log_file = os.path.join(os.getcwd(), "logs.log")

    logger = logging.getLogger("WhatsApp-Scrapper")
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(log_file)
    console_handler = logging.StreamHandler()

    formatter = logging.Formatter(fmt="%(asctime)s - [%(levelname)s] - %(message)s", datefmt="%d/%m/%Y %H:%M:%S")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.propagate = False

    return logger

if __name__ == "__main__":
    log = logger() # Setup logger
    main()