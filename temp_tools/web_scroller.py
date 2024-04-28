from selenium import webdriver
import time

# Initialize the web driver (make sure you have the appropriate driver installed and added to PATH)
driver = webdriver.Chrome()

# Open the desired webpage
driver.get(r"C:\Users\sangha\Documents\Danny's\SloDictGen\data\html\sskj\si_sskj.html")

# Scroll down the page gradually
scroll_pause_time = 1  # Adjust this value as needed
screen_height = driver.execute_script("return window.screen.height;")
i = 1
while True:
    # Scroll down to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait for the page to load
    time.sleep(scroll_pause_time)
    # Calculate new scroll height and compare with the last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == screen_height:
        break
    screen_height = new_height
    i += 1

# Close the browser
driver.quit()
