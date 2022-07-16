from main_functions import *

url = 'https://pyckio.com/i/#!rankings'
main_data = {'Имя Каппера': [], 'Сcылка на канал': [], 'Количество ставок': [], 'Roi(Yield на некоторых сайтах) %': [],
             'Profit': [], 'Ср. Кф за все ставки': [], 'Winrate(%)': [], 'Ставки': []}

links = []
number_list = []


def get_links():
    driver = create_driver()
    driver.get(url)
    for i in range(100):
        scroll_down(driver)
    time.sleep(5)
    html = get_html_sel(driver)
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find('div', 'panel-body').find_all('tr')
    for item in items:
        try:
            link = 'https://pyckio.com/i/' + item.find('a').get('href')
            print(link)
            number = item.find_all('td')[8].text
            print(number)
            if int(number) >= 500:
                links.append(link)
                number_list.append(number)
        except:
            print('no')
    return driver


def get_publish_date(driver):
    list_years = ['2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010',
                  '2009', '2008', '2007', '2006']
    months = ['August', 'July', 'June', 'May', 'April', 'February', 'January']
    data = 'yes'
    last_page = driver.current_url
    scroll_down(driver)
    time.sleep(4)
    html3 = get_html_sel(driver)
    soup3 = BeautifulSoup(html3, 'lxml')
    driver.find_element_by_xpath('//*[@id="content"]/div/div/ul/li[1]/a').click()
    linkk = 'https://pyckio.com/i/' + soup3.find_all('tr')[-80].find_all('td')[2].find('a').get('href')
    print(linkk)
    driver.get(linkk)
    time.sleep(4)
    html4 = get_html_sel(driver)
    soup4 = BeautifulSoup(html4, 'lxml')
    publish_date = soup4.find('div','date').find_all(text=True)[0].replace('\n','').strip()
    print(publish_date)
    driver.get(last_page)
    time.sleep(3)
    if '2021' in publish_date:
        for month in months:
            if month in publish_date:
                data = 'nope'
                break
    for year in list_years:
        if year in publish_date:
            data = 'nope'
            break
    return data


def parse_data(driver):
    links = ['https://pyckio.com/i/#!account/motaliz/soccer']
    number_list = ['2660']
    for link, numba in zip(links, number_list):
        spisok = []
        driver.get(link)
        time.sleep(7)
        html2 = get_html_sel(driver)
        soup2 = BeautifulSoup(html2, 'lxml')
        name_capper = str(soup2.find('div', 'panel-heading pro-user').find_next('a').find_all(text=True)[2])
        print(name_capper)
        link_capper = link
        col_stav = numba
        roi_yield = soup2.find('div', 'stats follow-button').find_all(text=True)[16]
        print(roi_yield)
        middle_kf = soup2.find_all('tr', 'global')[-1].find_all(text=True)[-2]
        print(middle_kf)
        winrate = soup2.find_all('tr', 'global')[-1].find_all(text=True)[-6]
        print(winrate)
        data = get_publish_date(driver)
        if data == 'nope': break
        time.sleep(3)
        scroll_down(driver)
        driver.find_element_by_xpath('//*[@id="content"]/div/div/ul/li[1]/a').click()
        for i in range(16):
            scroll_down(driver)
            time.sleep(1.5)
        items2 = driver.find_elements_by_tag_name('tr')[1282:]
        print(items2)
        for item2 in items2:
            stav = item2.find_elements_by_tag_name('td')[2].find_element_by_tag_name('a').text + ' ' + \
                   item2.find_elements_by_tag_name('td')[4].text
            kf = item2.find_element_by_class_name('text-right').text
            publish_date = item2.find_elements_by_tag_name('td')[3].text
            link_post = item2.find_elements_by_tag_name('td')[2].find_element_by_tag_name('a').get_attribute('href')
            try:
                result = item2.find_element_by_class_name('text-right text-success')
            except:
                result = 'Lose'
            else:
                result = 'Win'
            end = {'Ставка': stav.strip(), 'КФ': kf,
                   'Букмекер': 'unknown',
                   'Время публикации': publish_date.strip(),
                   'Ссылка на пост': link_post, 'Результат': result.strip()}
            spisok.append(end)
        main_data['Имя Каппера'].append(name_capper)
        main_data['Сcылка на канал'].append(link_capper)
        main_data['Количество ставок'].append(col_stav)
        main_data['Roi(Yield на некоторых сайтах) %'].append(roi_yield)
        main_data['Ср. Кф за все ставки'].append(middle_kf)
        main_data['Winrate(%)'].append(winrate)
        main_data['Ставки'].append(spisok)


def long():
    driver = get_links()
    parse_data(driver)
    save_data('Pyckio.xlsx', main_data)


long()
