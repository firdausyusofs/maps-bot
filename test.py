from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ChromeOptions, ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import re
from os.path import exists

diff_x = 0.0179815292
diff_y = 0.009437118


orig_y = 2.5919824729117695
orig_x = 101.055703
zoom_level = 16

opts = ChromeOptions()
# opts.add_argument("--window-size=2560,1440")
opts.add_argument("--start-maximized")
opts.add_experimental_option("useAutomationExtension", False)
opts.add_experimental_option("excludeSwitches",["enable-automation"])

driver = webdriver.Chrome(options=opts)
wait = WebDriverWait(driver=driver, timeout=20)
# driver.get(f"https://www.google.com/maps")
driver.get(f"https://www.google.com/maps/@{orig_y},{orig_x},{zoom_level}z/data=!5m2!1e1!1e4")
# driver.get(f"https://www.google.com/maps/place//@{orig_y},{orig_x},{zoom_level}z/data=!4m5!3m4!1s0x0:0xe06a982b9a46c93a!8m2!3d3.152991!4d101.6212141!5m2!1e4!1e1")
wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="content-container"]/div[23]/div[1]/div[2]')))
wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="layer"]/div/div/div')))
wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="layer"]/div/div/div/span/span[1]/div')))
live = driver.find_element(By.XPATH, '//*[@id="layer"]/div/div/div/span/span[1]/div').click()
wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id=":1"]/div'))).click()
wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="layer"]/div/div/div/div/div[1]/div[1]/button[3]'))).click()
wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="layer"]/div/div/div/div/div[2]/div/div[1]/span[2]')))

hour = driver.find_element(By.XPATH, '//*[@id="layer"]/div/div/div/div/div[2]/div/div[1]/span[2]')
hour.click()

for i in range(1, 7):
    # time.sleep(1)
    actions = ActionChains(driver)
    actions.send_keys(Keys.LEFT)
    actions.perform()

# wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchboxinput"]')))
# search = driver.find_element(By.XPATH, '//*[@id="searchboxinput"]')

# btn = driver.find_element(By.XPATH, 'xpath///*[@id=":2"]')
# btn.click()
# document.querySelector("#QA0Szd > div > div > div.gYkzb").remove()
driver.execute_script("""
    document.querySelector("#omnibox-container").hidden = true
    document.querySelector("#content-container > div.app-viewcard-strip.ZiieLd").hidden = true
    document.querySelector("#content-container > div.scene-footer-container.Hk4XGb").hidden = true
    document.querySelector("#gb > div > div").hidden = true
    document.querySelector("#assistive-chips").hidden = true
    document.querySelector("#gb > div").hidden = true
    document.querySelector("#interactive-hovercard").remove()
""")

def save_screenshot(count, driver):
    time.sleep(1)
    driver.save_screenshot(f"{count}.png")
    url = driver.current_url
    c = re.search("\d+((.|,)\d+),\d+((.|,)\d+)", url)
    coord = c[0]
    with open(f"{count}.txt", 'w') as f:
            f.write(coord)
            f.close()

# count = 0
# for i in range(10):
#     x = orig_x + (diff_x*i)
#     search.clear()
#     search.send_keys(f"{orig_y}, {x}" + "\n")
#     driver.save_screenshot(f"{count}.png")
#     count = count + 1

# Drag and screenshot
count = 0
for i in range(45):
    canvas_element = driver.find_element(By.XPATH, '//*[@id="scene"]/div[3]/canvas')
    width =  int(canvas_element.size['width'])
    height = int(canvas_element.size["height"])
    actions = ActionChains(driver)
    
    if i == 0:
        save_screenshot(count, driver)
        count = count + 1
    else:
        for k in range(2):
            actions.move_to_element(canvas_element).click_and_hold().move_by_offset(0, -height/2).release(canvas_element).perform()
        save_screenshot(count, driver)
        count = count + 1

    for j in range(20):
        next_pos = width
        if (i % 2) != 0:
            next_pos = -width
        for k in range(2):
            actions.move_to_element(canvas_element).click_and_hold().move_by_offset(next_pos/2, 0).release(canvas_element).perform()
        save_screenshot(count, driver)
        count = count + 1
    
# for i in range(40):
#     canvas_element = driver.find_element(By.XPATH, '//*[@id="scene"]/div[3]/canvas')
#     width =  int(canvas_element.size['width'])
#     height = int(canvas_element.size["height"])
#     actions = ActionChains(driver)
#     actions.move_to_element(canvas_element).click_and_hold().move_by_offset(width, 0).release(canvas_element).perform()

    # actions.move_to_element_with_offset(canvas_element, width, 0).click().perform()
# for i in range(98):
#     y = orig_y + (diff_y*i)
#     for j in range(48):
#         if exists(f"{count}.png"):
#             count = count + 1
#             continue

#         x = orig_x + (diff_x*j)
#         driver.get(f"https://www.google.com/maps/@{y},{x},{zoom_level}z/data=!5m2!1e1!1e4")
#         # wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="minimap"]/div/div[2]/button')))
#         # layer = driver.find_element(By.XPATH, '//*[@id="minimap"]/div/div[2]/button')
#         # layer.click()
#         wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="content-container"]/div[23]/div[1]/div[2]')))
#         wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="layer"]/div/div/div')))
#         wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="layer"]/div/div/div/span/span[1]/div')))
#         live = driver.find_element(By.XPATH, '//*[@id="layer"]/div/div/div/span/span[1]/div').click()
#         wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id=":1"]/div'))).click()
#         wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="layer"]/div/div/div/div/div[1]/div[1]/button[3]'))).click()
#         wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="layer"]/div/div/div/div/div[2]/div/div[1]/span[2]')))

#         hour = driver.find_element(By.XPATH, '//*[@id="layer"]/div/div/div/div/div[2]/div/div[1]/span[2]')
#         hour.click()

#         for i in range(1, 7):
#             # time.sleep(1)
#             actions = ActionChains(driver)
#             actions.send_keys(Keys.LEFT)
#             actions.perform()
#         # btn = driver.find_element(By.XPATH, 'xpath///*[@id=":2"]')
#         # btn.click()
#         driver.execute_script("""
#         document.querySelector("#omnibox-container").hidden = true
#         document.querySelector("#content-container > div.app-viewcard-strip.ZiieLd").hidden = true
#         document.querySelector("#content-container > div.scene-footer-container.Hk4XGb").hidden = true
#         document.querySelector("#gb > div > div").hidden = true
#         document.querySelector("#assistive-chips").hidden = true
#         document.querySelector("#gb > div").hidden = true
#         """)

#         driver.save_screenshot(f"{count}.png")
#         with open(f"{count}.txt", 'w') as f:
#             f.write(f"{y},{x}")
#             f.close()

#         count = count+1

driver.close()