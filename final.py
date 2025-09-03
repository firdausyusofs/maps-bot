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


def datetime_range(start, end, delta):
    current = start
    while current <= end:
        yield current
        current += delta


def create_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path)

coordinates = {}

def save_screenshot(count, driver, day, formated_time, proper_formatted_time):
    driver.execute_script('''
        if (document.getElementById('popup')) {
            document.querySelector('#popup').remove()
        }
    ''')
    time.sleep(1)
    driver.save_screenshot(f"./images/{day}/{formated_time}/{formated_time}_{count}.png")
    url = driver.current_url
    c = re.search("\\d+((.|,)\\d+),\\d+((.|,)\\d+)", url)
    if c == None:
        return
    coord = c[0]
    if count == 0:
        coordinates[proper_formatted_time] = [coord]
    elif count == 3:
        coordinates[proper_formatted_time].append(coord)

    with open(f"./images/{day}/{formated_time}/{formated_time}_{count}.txt", 'w') as f:
            f.write(coord)
            f.close()


diff_x = 0.04119870000000958
diff_y = 0.01862190000000119

orig_y = 10.269274
orig_x = 123.721414
zoom_level = 17

#notifier = TelegramNotifier()

opts = ChromeOptions()
opts.add_argument("--start-maximized")
opts.add_experimental_option("useAutomationExtension", False)
opts.add_experimental_option("excludeSwitches", ["enable-automation"])

service = Service('./chromedriver')

driver = webdriver.Chrome(service=service, options=opts)
wait = WebDriverWait(driver=driver, timeout=20)

driver.get(f"https://www.google.com/maps/@{orig_y},{orig_x},{zoom_level}z/data=!5m2!1e1!1e4")
time.sleep(5)

wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="QA0Szd"]/div/div/div/div[1]/ul/li[1]/button')))
menu_button = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div/div[1]/ul/li[1]/button')
menu_button.click()

wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="settings"]/div/div[2]/ul/div[3]/li/div/button')))
driver.find_element(By.XPATH, '//*[@id="settings"]/div/div[2]/ul/div[3]/li/div/button').click()
driver.find_element(By.XPATH, '//*[@id="settings"]/div/div[2]/ul/div[2]/button').click()


driver.execute_script("""
    document.querySelector("#omnibox-container").hidden = true
    document.querySelector("#content-container > div.scene-footer-container.Hk4XGb").hidden = true
    document.querySelector("#gb > div > div").hidden = true
    document.querySelector("#assistive-chips").hidden = true
    document.querySelector("#gb > div").hidden = true
    document.querySelector("#interactive-hovercard").remove()
""")

actions = ActionChains(driver)
driver.execute_script('''
    document.querySelector("#content-container > div.app-viewcard-strip.ZiieLd").hidden = true
''')

i = 0

def run(i, now, row, col):
    day = now.strftime("%A")
    formated_time = f"{now.hour}_{now.minute}"
    proper_formatted_time = now.strftime("%H:%M")

    create_dir('./images/'+day+'/'+formated_time)

    actions.release().perform()

    count = 0

    total_time = 0

    # Drag and screenshot
    count = 0

    total_time = 0

    if i % 2 == 0:
        for j in range(row):
            start_time = time.time()
            canvas_element = driver.find_element(By.XPATH, '//*[@id="scene"]/div[3]/canvas')
            width =  int(canvas_element.size['width'])
            height = int(canvas_element.size["height"])

            if j == 0:
                save_screenshot(count, driver, day, formated_time, proper_formatted_time)
                count = count + 1
            else:
                for k in range(2):
                    actions.move_to_element(canvas_element).click_and_hold().move_by_offset(0, -height/2).release(canvas_element).perform()
                save_screenshot(count, driver, day, formated_time, proper_formatted_time)
                count = count + 1

            for m in range(col):
                next_pos = width
                if (j % 2) != 0:
                    next_pos = -width
                for k in range(2):
                    actions.move_to_element(canvas_element).click_and_hold().move_by_offset(next_pos/2, 0).release(canvas_element).perform()
                save_screenshot(count, driver, day, formated_time, proper_formatted_time)
                count = count + 1
            end_time = time.time()
            print(f"Time taken for iteration {j} (even index): {end_time - start_time} seconds")
            total_time += (end_time - start_time)
            i = i + 1
    else:
        for j in range(row):
            start_time = time.time()
            canvas_element = driver.find_element(By.XPATH, '//*[@id="scene"]/div[3]/canvas')
            width =  int(canvas_element.size['width'])
            height = int(canvas_element.size["height"])

            if j == 0:
                save_screenshot(count, driver, day, formated_time, proper_formatted_time)
                count = count + 1
            else:
                for k in range(2):
                    actions.move_to_element(canvas_element).click_and_hold().move_by_offset(0, height/2).release(canvas_element).perform()
                save_screenshot(count, driver, day, formated_time, proper_formatted_time)
                count = count + 1

            for m in range(col):
                next_pos = -width
                if (j % 2) != 0:
                    next_pos = width
                for k in range(2):
                    actions.move_to_element(canvas_element).click_and_hold().move_by_offset(next_pos/2, 0).release(canvas_element).perform()
                save_screenshot(count, driver, day, formated_time, proper_formatted_time)
                count = count + 1
            end_time = time.time()
            print(f"Time taken for iteration {j} (odd index): {end_time - start_time} seconds")
            total_time += (end_time - start_time)
            i = i + 1

    # notifier.notify(f'Done ({day}): {proper_formatted_time} - {coordinates[proper_formatted_time][0]} to {coordinates[proper_formatted_time][1]}')
    print(f'Total time for {day} {proper_formatted_time}: {total_time} seconds')

is_running = False
i = 0
now = datetime.datetime.now()
run(i, now, 19, 11)

driver.close()
