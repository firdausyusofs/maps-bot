from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ChromeOptions, ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import math

opts = ChromeOptions()
opts.add_argument("--start-maximized")
opts.add_experimental_option("useAutomationExtension", False)
opts.add_experimental_option("excludeSwitches", ["enable-automation"])

driver = webdriver.Chrome(options=opts)
wait = WebDriverWait(driver=driver, timeout=20)

orig_y = 2.5919824729117695
orig_x = 101.055703
dest_y = 3.513467
dest_x = 101.90468846468413

zoom_level = 16

driver.get(f"https://www.google.com/maps/@{orig_y},{orig_x},{zoom_level}z/data=!5m2!1e1!1e4")

actions = ActionChains(driver)

driver.get(f"https://www.google.com/maps/@{orig_y},{orig_x},{zoom_level}z/data=!5m2!1e1!1e4")
wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="content-container"]/div[23]/div[1]/div[2]')))
wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="layer"]/div/div/div')))
wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="layer"]/div/div/div/span/span[1]/div')))
live = driver.find_element(By.XPATH, '//*[@id="layer"]/div/div/div/span/span[1]/div').click()
wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id=":1"]/div'))).click()
wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="layer"]/div/div/div/div/div[2]/div/div[1]/span[2]')))

canvas_element = driver.find_element(By.XPATH, '//*[@id="scene"]/div[3]/canvas')
width =  int(canvas_element.size['width'])
height = int(canvas_element.size["height"])

# for k in range(2):
#     actions.move_to_element(canvas_element).click_and_hold().move_by_offset(width/2, 0).release(canvas_element).perform()

for k in range(2):
    actions.move_to_element(canvas_element).click_and_hold().move_by_offset(0, -height/2).release(canvas_element).perform()

time.sleep(1)

for k in range(2):
    actions.move_to_element(canvas_element).click_and_hold().move_by_offset(width/2, 0).release(canvas_element).perform()

time.sleep(1)

url = driver.current_url
c = re.search("\d+((.|,)\d+),\d+((.|,)\d+)", url)
c2 = c[0]

c2 = c2.split(",")

diff_y = float(c2[0]) - orig_y
diff_x = float(c2[1]) - orig_x

diff_cord_y = dest_y - orig_y
diff_cord_x = dest_x - orig_x

row = math.ceil(diff_cord_y / diff_y)
column = math.ceil(diff_cord_x / diff_x)

print(row)
print(column)
