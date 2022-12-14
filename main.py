from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ChromeOptions, ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from os.path import exists

diff_x = 0.0179815292
diff_y = 0.009437118


orig_y = 2.5919824729117695
orig_x = 101.055703
zoom_level = 17

opts = ChromeOptions()
opts.add_argument("--window-size=2560,1440")
opts.add_experimental_option("useAutomationExtension", False)
opts.add_experimental_option("excludeSwitches",["enable-automation"])

driver = webdriver.Chrome(options=opts)
wait = WebDriverWait(driver=driver, timeout=20)
# driver.get(f"https://www.google.com/maps")

count = 0
for i in range(98):
    y = orig_y + (diff_y*i)
    for j in range(48):
        if exists(f"{count}.png"):
            count = count + 1
            continue

        x = orig_x + (diff_x*j)
        driver.get(f"https://www.google.com/maps/@{y},{x},{zoom_level}z/data=!5m2!1e1!1e4")
        # wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="minimap"]/div/div[2]/button')))
        # layer = driver.find_element(By.XPATH, '//*[@id="minimap"]/div/div[2]/button')
        # layer.click()
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
        # btn = driver.find_element(By.XPATH, 'xpath///*[@id=":2"]')
        # btn.click()
        driver.execute_script("""
        document.querySelector("#omnibox-container").hidden = true
        document.querySelector("#content-container > div.app-viewcard-strip.ZiieLd").hidden = true
        document.querySelector("#content-container > div.scene-footer-container.Hk4XGb").hidden = true
        document.querySelector("#gb > div > div").hidden = true
        document.querySelector("#assistive-chips").hidden = true
        document.querySelector("#gb > div").hidden = true
        """)

        driver.save_screenshot(f"{count}.png")
        with open(f"{count}.txt", 'w') as f:
            f.write(f"{y},{x}")
            f.close()

        count = count+1

driver.close()