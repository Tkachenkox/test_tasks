'''

Task:
1)Go to the off site Udemy
2)Find Learn Flutter & Dart to Build iOS & Android Apps Course
3)Parse using any programming language the names of all free video tutorials (Introduction,What is Flutter?)
4)Pour code into a new repository on Git (GitHub, GitLab, BitBucket or others)
Complications:
Sort the sheet by video length (also found on the site)

'''

import time
import re
import requests
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup

class Parser():
    

    def __init__(self):
        self.FILENAME = 'stat.csv'
        self.URLS = ['https://www.udemy.com/courses/search/?price=price-free&q=flutter&sort=relevance',
                     'https://www.udemy.com/courses/search/?price=price-free&q=dart&sort=relevance']
        self.fox = 'geckodriver.exe'
        self.options = webdriver.FirefoxOptions()
        self.options.add_argument('headless')
        self.browser = webdriver.Firefox(executable_path=self.fox, firefox_options=self.options)
        self.links = []
        self.fin_arr = []
        self.counter = 0
        file = open('data.txt', 'w', encoding='utf-8')
        file.close()


    def get_links(self):
        for urls in self.URLS:
            self.browser.get(urls)
            # Поиск тегов по имени
            time.sleep(2)
            elements = self.browser.find_elements_by_class_name('udlite-custom-focus-visible')
            
            for elem in elements:
                self.links.append(elem.get_attribute('href'))
            
            
            for i in self.links:
                self.parse(i)
        
        self.browser.close()


    def parse(self, url):
        HEADERS = {
                    "Accept":"application/json, text/plain, */*",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language":"ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
                    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0"}
        
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        names = soup.find_all('span', class_='section--item-title--2k1DQ')
        durations = soup.find_all('span', class_='section--hidden-on-mobile--171Q9 section--item-content-summary--126oS')
        data = []
        total_dur = 0
        for i in range(len(names)):
            if re.search(r'\d\d:\d\d', str(durations[i])):
                dur = float(str(durations[i].text[0:2]) + '.' + str(durations[i].text[3:]))
                total_dur += dur
                data.append(names[i].text)
                data.append(dur)
                self.fin_arr.append(data)
                data = []
        self.fin_arr.sort(key = lambda i: i[1])
        print(url)
        file = open('data.txt', 'a', encoding='utf-8')
        file.write(url)
        for i in self.fin_arr:
            name_to_write = '\n' + str(i[0]) + ' '
            file.write(name_to_write)
            file.write(str(i[1]))
            file.write('\n')
        self.fin_arr = []


p = Parser()
p.get_links()