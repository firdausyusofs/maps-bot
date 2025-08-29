from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ChromeOptions, ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time
import re
from os.path import exists
import datetime
import os
from config import DayConfig, CoordinateData
import argparse

def create_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path)

# Set up the chrome driver
opts = ChromeOptions()
opts.add_argument("--start-maximized")
opts.add_experimental_option("useAutomationExtension", False)
opts.add_experimental_option("excludeSwitches", ["enable-automation"])

service = Service('./chromedriver')

driver = webdriver.Chrome(service=service, options=opts)
wait = WebDriverWait(driver=driver, timeout=20)

# Variables
day_config = DayConfig()

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--day', type=str, help='Day to run bot for', default='Monday')
parser.add_argument('--start_coordinate', type=str, help='Start coordinate, Ex: 10.269274,123.721414', default='')
parser.add_argument('--end_coordinate', type=str, help='End coordinate, Ex: 10.269274,123.721414', default='')
parser.add_argument('--zoom_level', type=int, help='Zoom level', default=16)
args = parser.parse_args()

try:
    day_config.get_day_config(args.day)
    coordinates = CoordinateData(args.start_coordinate, args.end_coordinate)

    # Get to tjhe map
    driver.get(f"https://www.google.com/maps/@{coordinates.start.lat},{coordinates.start.lat},{args.zoom_level}z/data=!5m2!e1!1e4?entry=ttu&g_ep=EgoyMDI1MDgyNS4wIKXMDSoASAFQAw%3D%3D")
    time.sleep(5)

    # Wait for the map to load
    live = driver.find_element(By.XPATH, '//*[@id="layer"]/div/div/span/span[1]/div').click()
    wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='map-canvas']")))

    # Hide elements
    driver.execute_script("""
        document.querySelector("#omnibox-container").hidden = true
        document.querySelector("#content-container > div.scene-footer-container.Hk4XGb").hidden = true
        document.querySelector("#gb > div > div").hidden = true
        document.querySelector("#assistive-chips").hidden = true
        document.querySelector("#gb > div").hidden = true
        document.querySelector("#interactive-hovercard").remove()
    """)


except ValueError:
    print('Invalid coordinate')
    exit(1)
except KeyError:
    print('Invalid day')
    exit(1)
