from selenium import webdriver
DRIVER = webdriver.Chrome(executable_path="/Users/riobeggs/Documents/chromedriver-2")
INVALID_URL = True

def run_web_driver():
    while INVALID_URL:
        url = input("Enter URL: ")
        print("\nDecoding...\n")
        try:
            DRIVER.get(url)
            return DRIVER
        except:
            continue