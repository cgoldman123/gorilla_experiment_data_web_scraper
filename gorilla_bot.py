from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException

def run_bot():
    # get carter's username and password for gorilla
    with open('carter_gorilla_email.txt', 'r') as file:
        carter_gorilla_email = file.read().strip()
    with open('carter_gorilla_password.txt', 'r') as file:
        carter_gorilla_pass = file.read().strip()        
    
    # Initialize the driver
    driver = webdriver.Chrome(ChromeDriverManager().install())


    # Navigate to the website
    driver.get("https://app.gorilla.sc/login")
    time.sleep(4)
    # close cookies button
    cookies_button = driver.find_element(By.ID, "request-marketing-accept")
    cookies_button.click()
    # Login
    username = driver.find_element(By.ID, "email")
    password = driver.find_element(By.ID, "password")
    username.send_keys(carter_gorilla_email)
    password.send_keys(carter_gorilla_pass)
    login_button = driver.find_element(By.ID, "login-button")
    login_button.click()
    time.sleep(4)
    # navigate to the data page
    driver.get("https://app.gorilla.sc/admin/experiment/169510/data")
    # open the data download popup
    data_button = driver.find_element(By.ID, "data-button")
    data_button.click()
    time.sleep(15)
    # Regenerating data 
    regen_button = driver.find_element(By.CLASS_NAME, "button-build")
    regen_button.click()
    time.sleep(15)
    # close the popup
    close_button = driver.find_element(By.CLASS_NAME, "close")
    close_button.click()
    time.sleep(10)
    # refresh the page
    driver.get("https://app.gorilla.sc/admin/experiment/169510/data")

    # download the data
    found_download_button = False
    while found_download_button == False:
        try:
            data_button = driver.find_element(By.ID, "data-button")
            # open the data download popup
            data_button.click()
            time.sleep(8)
            # Try to find the download button
            download_button = driver.find_element(By.CLASS_NAME, "button-download")
            # If the button is found, you can perform actions on it
            found_download_button = True
        except NoSuchElementException:
            # If the button is not found, refresh the page
            print("Download button not found, refreshing the page.")
            driver.refresh()
            time.sleep(20)

    download_button.click()
    time.sleep(500)
    # # Close the driver
    # driver.quit()
    driver.quit()

