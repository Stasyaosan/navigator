from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from selenium.webdriver.chrome.options import Options

from time import sleep
import json
from selenium import webdriver
import django

django.setup()
from .models import Link
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def parser():
    django.setup()
    ll = Link.objects.all()
    links_global = []
    for q in ll:
        links_global.append(q.link)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Remote(
        command_executor='http://chrome:4444/wd/hub',
        options=chrome_options
    )
    # driver = webdriver.Chrome()
    for i in links_global:
        driver.get(i)
        day_of_week = driver.title.split(' - ')[1]
        print(day_of_week)
        scroll_global = 0

        def scroll_down():
            view_container = driver.find_element(By.CLASS_NAME, 'light-scrollbar')

            c_h = driver.execute_script("arguments[0].scrollTop += 500; return arguments[0].scrollTop;", view_container)
            driver.execute_script("arguments[0].scrollHeight;", view_container)
            ht = driver.execute_script("""
                       return arguments[0].scrollHeight;
                       """, view_container)
            sleep(1)
            return c_h, ht

        try:
            WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#viewContainer"))
            )
            # day_of_week = driver.find_elements(By.CLASS_NAME, 'top-bar-text-light-primary-hover-forced')[0].text

            new = []
            count = 0
            # div_title = driver.find_elements(By.TAG_NAME, 'title')
            # for el in div_title:
            #    print(el.)

            while True:
                div_teacher_z = driver.find_elements(By.CSS_SELECTOR, '''
                
                div[title='форма'], 
                div[title='время'], 
                div[title='группа'], 
                div[title='состав группы'], 
                div[title='предмет'], 
                div[title='учитель'], 
                div[title='кабинеты'], 
                div[title='ссылка для подключения'],
                div[title='учитель на замену'],
                div[title='ссылка на замену']
                ''')
                row = []

                for el in div_teacher_z:
                    next_1 = el.find_elements(By.XPATH, 'following-sibling::div[1]')

                    for n in next_1:
                        row.append(n.text)
                        # count += 1
                    count += 7
                new.append(row)
                a1, a2 = scroll_down()
                if scroll_global == a1:
                    break
                scroll_global = a1
            nnn = []
            for ne in new:
                if not ne in nnn:
                    nnn.append(ne)
            nnn_dict = {}

            for ni in nnn:
                for ini in range(0, len(ni), 10):
                    if ni[ini + 1] in nnn_dict:
                        pass
                    else:
                        nnn_dict[ni[ini + 1]] = [
                            day_of_week, ni[ini], ni[ini + 2], ni[ini + 3], ni[ini + 4], ni[ini + 5], ni[ini + 6],
                            ni[ini + 7],
                            ni[ini + 8], ni[ini + 9]
                        ]
            open(f'/workapp/app/json/{day_of_week}.json', 'w').write(json.dumps(nnn_dict))
        except:
            pass
