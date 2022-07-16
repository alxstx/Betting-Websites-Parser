from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import xlsxwriter


def create_driver():
    driver1 = webdriver.Chrome(executable_path='/Users/alex/Downloads/chromedriver')
    return driver1


def get_html_sel(driver):
    try:
        html = driver.page_source
    except:
        html = 'Error'
        print(html)
    return html


def scroll_down(driver):
    html = driver.find_element_by_tag_name('html')
    html.send_keys(Keys.END)


def scroll_up(driver):
    html = driver.find_element_by_tag_name('html')
    html.send_keys(Keys.PAGE_UP)


def scroll_down2(driver):
    html = driver.find_element_by_tag_name('html')
    html.send_keys(Keys.PAGE_DOWN)


def save_data(nameexcel, data):
    workbook = xlsxwriter.Workbook(nameexcel)
    worksheet = workbook.add_worksheet('Воркшит намбер 1')
    for i, d in enumerate(list(data.keys())[:-1]):
        worksheet.write(0, i, d)
    for k, l in enumerate(list(data.values())[-1]):
        if k == 0:
            new = l.keys()
            for j, n in enumerate(new):
                worksheet.write(0, len(list(data.keys())[:-1]) + j, n)
    for i1, d1 in enumerate(list(data.values())[:-1]):
        for ii, dd in enumerate(d1):
            worksheet.write(ii + 1, i1, dd)
    for k1, l1 in enumerate(list(data.values())[-1]):
        new1 = l1.values()
        for jj, ni in enumerate(new1):
            worksheet.write(k1+1,len(list(data.keys())[:-1]) + jj, ni)
    workbook.close()


