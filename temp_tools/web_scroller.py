import pyautogui
import time

sites = [f"https://uncle-ayiro.github.io/SloDictGen/data/html/sskj/si_sskj_split/si_sskj_{num}.html"
         for num in range(1, 4)]

# Delay before starting (in seconds)
initial_delay = 5
# Delay between each scroll action (in seconds)
scroll_delay = 0.01
# Number of scrolls
num_scrolls = 200000

# Wait for the initial delay before starting
time.sleep(initial_delay)

# Loop to simulate scrolling
for _ in range(num_scrolls):
    # Simulate a mouse click to focus on the browser window
    #pyautogui.click()
    # Scroll down by moving the mouse wheel
    pyautogui.scroll(-75)
    # Wait for the scroll delay
    time.sleep(scroll_delay)
