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
#from telegram_notifier import TelegramNotifier


def datetime_range(start, end, delta):
    current = start
    while current <= end:
        yield current
        current += delta


def create_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path)


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

map_initial_time = datetime.datetime.now().replace(hour=8, minute=55, second=0, microsecond=0)
all_days = {'Sunday': 1, 'Monday': 2, 'Tuesday': 3, 'Wednesday': 4, 'Thursday': 5, 'Friday': 6, 'Saturday': 7}

days = ["Friday"]
interval = 30
start_time = datetime.datetime.now().replace(hour=6, minute=0, second=0, microsecond=0)
end_time = datetime.datetime.now().replace(hour=22, minute=0, second=0, microsecond=0)
time_range = [dt for dt in datetime_range(start_time, end_time, datetime.timedelta(minutes=interval))]

driver.get(f"https://www.google.com/maps/@{orig_y},{orig_x},{zoom_level}z/data=!5m2!1e1!1e4")
time.sleep(5)

#wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="content-container"]/div[23]/div[1]/div')))
#wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="layer"]/div/div/div')))
#wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="layer"]/div/div/span/span[1]/div')))
#live = driver.find_element(By.XPATH, '//*[@id="layer"]/div/div/span/span[1]/div').click()
#wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id=":1"]/div'))).click()
#wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="layer"]/div/div/div/div/div[2]/div/div[1]/span[2]')))
driver.execute_script("""
    document.querySelector("#omnibox-container").hidden = true
    document.querySelector("#content-container > div.scene-footer-container.Hk4XGb").hidden = true
    document.querySelector("#gb > div > div").hidden = true
    document.querySelector("#assistive-chips").hidden = true
    document.querySelector("#gb > div").hidden = true
    document.querySelector("#interactive-hovercard").remove()
""")

coordinates = {}

def save_screenshot(count, driver):
    driver.execute_script('''
        if (document.getElementById('popup')) {
            document.querySelector('#popup').remove()
        }
    ''')
    time.sleep(1)
    driver.save_screenshot(f"./images2/{day}/{formatted_time}/{formatted_time}_{count}.png")
    url = driver.current_url
    c = re.search("\d+((.|,)\d+),\d+((.|,)\d+)", url)
    coord = c[0]
    if count == 0:
        coordinates[proper_formatted_time] = [coord]
    elif count == 3:
        coordinates[proper_formatted_time].append(coord)

    with open(f"./images2/{day}/{formatted_time}/{formatted_time}_{count}.txt", 'w') as f:
            f.write(coord)
            f.close()

fn = '''
    function clickOnElem(elem, offsetX, offsetY) {
        var rect = elem.getBoundingClientRect(),
            posX = rect.left, posY = rect.top; // get elems coordinates
        // calculate position of click
        if (typeof offsetX == 'number') posX += offsetX;
        else if (offsetX == 'center') {
            posX += rect.width / 2;
            if (offsetY == null) posY += rect.height / 2;
        }
        if (typeof offsetY == 'number') posY += offsetY;
        // create event-object with calculated position
        var evt = new MouseEvent('click', {bubbles: true, clientX: posX, clientY: posY});
        elem.dispatchEvent(evt); // trigger the event on elem
    }
'''

actions = ActionChains(driver)
for idx, day in enumerate(days):
    create_dir('./images2/'+day)
    driver.execute_script('''
        document.querySelector("#content-container > div.app-viewcard-strip.ZiieLd").hidden = false
    ''')
    # wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="layer"]/div/div/div/div[1]/div[1]/button[{all_days[day]}]'))).click()
    for i, dt in enumerate(time_range):
        actions.release().perform()
        formatted_time = f'{dt.hour}_{dt.minute}'
        proper_formatted_time = dt.strftime("%H:%M")
        # notifier.notify(f"Running ({day}): {proper_formatted_time} ({1.0666666667 * (i * 5.277*2)})")
        create_dir('./images2/'+day+'/'+formatted_time)
        driver.execute_script('''
            document.querySelector("#content-container > div.app-viewcard-strip.ZiieLd").hidden = false
        ''')

        string = f'''
            {fn}

            var diff = 1.0666666667 * (
        '''

        string += str(i)
        string += ' * 5.277)'

        string += '''
            var elem = document.querySelector("#layer > div > div > div > div.MtRpGc > div > div.alivie > span.o3K2jf")

            clickOnElem(elem, diff, 0)
        '''

        #driver.execute_script(string)

        driver.execute_script('''
            document.querySelector("#content-container > div.app-viewcard-strip.ZiieLd").hidden = true
        ''')

        # Drag and screenshot
        count = 0

        total_time = 0

        # Running for even index
        if i % 2 == 0:
            # for j in range(49):
            for j in range(19):
                start_time = time.time()
                canvas_element = driver.find_element(By.XPATH, '//*[@id="scene"]/div[3]/canvas')
                width =  int(canvas_element.size['width'])
                height = int(canvas_element.size["height"])
                
                if j == 0:
                    save_screenshot(count, driver)
                    count = count + 1
                else:
                    for k in range(2):
                        actions.move_to_element(canvas_element).click_and_hold().move_by_offset(0, -height/2).release(canvas_element).perform()
                    save_screenshot(count, driver)
                    count = count + 1

                for m in range(11):
                    next_pos = width
                    if (j % 2) != 0:
                        next_pos = -width
                    for k in range(2):
                        actions.move_to_element(canvas_element).click_and_hold().move_by_offset(next_pos/2, 0).release(canvas_element).perform()
                    save_screenshot(count, driver)
                    count = count + 1
                end_time = time.time()
                print(f"Time taken for iteration {j} (even index): {end_time - start_time} seconds")
                total_time += (end_time - start_time)

        # Running for odd index
        else:
            for j in range(19):
                start_time = time.time()
                canvas_element = driver.find_element(By.XPATH, '//*[@id="scene"]/div[3]/canvas')
                width =  int(canvas_element.size['width'])
                height = int(canvas_element.size["height"])

                if j == 0:
                    save_screenshot(count, driver)
                    count = count + 1
                else:
                    for k in range(2):
                        actions.move_to_element(canvas_element).click_and_hold().move_by_offset(0, height/2).release(canvas_element).perform()
                    save_screenshot(count, driver)
                    count = count + 1

                for m in range(11):
                    next_pos = -width
                    if (j % 2) != 0:
                        next_pos = width
                    for k in range(2):
                        actions.move_to_element(canvas_element).click_and_hold().move_by_offset(next_pos/2, 0).release(canvas_element).perform()
                    save_screenshot(count, driver)
                    count = count + 1
                end_time = time.time()
                print(f"Time taken for iteration {j} (odd index): {end_time - start_time} seconds")
                total_time += (end_time - start_time)

        # notifier.notify(f'Done ({day}): {proper_formatted_time} - {coordinates[proper_formatted_time][0]} to {coordinates[proper_formatted_time][1]}')
        print(f'Total time for {day} {proper_formatted_time}: {total_time} seconds')

    final_message = f'''
        Completed: {day}

    '''

    for i, v in coordinates.items():
        final_message += f'{i}: {v[0]} to {v[1]}\n'

    # notifier.notify(final_message, True)

driver.close()

