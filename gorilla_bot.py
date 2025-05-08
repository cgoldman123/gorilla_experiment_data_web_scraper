from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service

"""
===============================================================================
gorilla_bot.py

Automates the process of logging into the Gorilla.sc platform and downloading 
experiment data for a specific project.

Functionality:
- Reads Gorilla login credentials from local text files.
- Launches a Chrome browser instance using Selenium and WebDriverManager.
- Logs into the Gorilla admin portal.
- Navigates to a specific experiment's data page.
- Regenerates the dataset (to include new submissions).
- Waits for the regeneration process to complete.
- Initiates and downloads the most recent data as a .zip file.

Key Notes:
- Designed for use on Windows and Linux (adjusts file paths accordingly).
- The downloaded file is expected to appear in the user's Downloads folder.
- Uses a while loop to ensure the download button is available before proceeding.
- Sleeps are used for timing and can be adjusted depending on network speed and
  Gorilla server responsiveness.

Dependencies:
- selenium
- webdriver-manager

To run:
- Ensure Chrome is installed and compatible with ChromeDriverManager.
- Place credential text files (`carter_gorilla_email.txt`, `carter_gorilla_password.txt`) 
  in the specified directory (`L:/rsmith/wellbeing/tasks/QC/getting_gorilla_data/`).

===============================================================================
"""


def run_bot():
    # get carter's username and password for gorilla
    with open('L:/rsmith/wellbeing/tasks/QC/getting_gorilla_data/carter_gorilla_email.txt', 'r') as file:
        carter_gorilla_email = file.read().strip()
    with open('L:/rsmith/wellbeing/tasks/QC/getting_gorilla_data/carter_gorilla_password.txt', 'r') as file:
        carter_gorilla_pass = file.read().strip()        
    
    # Initialize the driver
    #driver = webdriver.Chrome(ChromeDriverManager().install())

    driver_path = ChromeDriverManager().install()
    if driver_path:
        driver_name = driver_path.split('/')[-1]
        # due to a chrome update, ChromeDriverManager().Install() returns a third party binaries file that we don't need. Change the file path before calling driver.
        if driver_name!="chromedriver":
            driver_path = "/".join(driver_path.split('/')[:-1]+["chromedriver"])
            #os.chmod(driver_path, 0o755) change permissions of file specified by driver_path
    driver = webdriver.Chrome(service=Service(driver_path))


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
            time.sleep(15)
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
    time.sleep(900)
    # # Close the driver
    # driver.quit()
    driver.quit()

# run_bot()