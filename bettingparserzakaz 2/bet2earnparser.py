from main_functions import *

url = 'https://bet2earn.com/tipsters'
main_data = {'Имя Каппера': [], 'Сcылка на канал': [], 'Количество ставок': [], 'Roi(Yield на некоторых сайтах) %': [],
             'Profit': [], 'Ср. Кф за все ставки': [], 'Winrate(%)': [], 'Ставки': []}
links = []
number_list = []


def get_links():
    driver = create_driver()
    driver.get(url)
    time.sleep(18)
    scroll_down(driver)
    thebutton = driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[2]/div[15]/button')
    thebutton.click()
    a = 15
    while thebutton != None:
        a += 10
        time.sleep(15)
        scroll_down(driver)
        time.sleep(1)
        try:
            thebutton = driver.find_element_by_xpath(f'//*[@id="root"]/div/div/div/div[2]/div[{str(a)}]/button')
        except:
            time.sleep(3)
            thebutton = driver.find_element_by_xpath(f'//*[@id="root"]/div/div/div/div[2]/div[{str(a)}]/button')
        thebutton.click()
    items = driver.find_elements_by_class_name('tipster')
    for item in items:
        link = item.find_element_by_tag_name('h2').find_element_by_tag_name('a').get_attribute('href')
        number = item.find_elements_by_class_name('t-centered')[3].text
        number = number[number.find('\n'):]
        if int(number) >= 500:
            links.append(link)
            number_list.append(number)
    return driver


def get_publish_date(driver):
    dop_words = ['a day ago', 'days ago', 'a month ago', '2 months ago', '3 months ago', '4 months ago', '5 months ago',
                 '6 months ago']
    publish_date = driver.find_element_by_xpath(
        '/html/body/div/div/div/div[2]/div/div[2]/div/div[2]/div/div[1]/div/div[2]/div[2]/span').text
    data = 'Yes'
    for i, dop in enumerate(dop_words):
        if dop in publish_date:
            break
        else:
            if i == 8:
                data = 'nope'
    return data


def parse_data(driver):
    links = ['https://bet2earn.com/tipsters/futbolinvisiblevip']
    number_list = ['1235']
    for link, numba in zip(links, number_list):
        spisok = []
        driver.get(link)
        time.sleep(10)
        name_capper = driver.find_element_by_tag_name('h1').find_element_by_tag_name('a').text
        link_capper = link
        col_stav = numba
        roi_yield = driver.find_element_by_class_name('mdirection').find_element_by_tag_name('strong').text
        profit = driver.find_element_by_class_name('mdirection').find_elements_by_tag_name('strong')[2].text
        winrate = driver.find_element_by_class_name('mdirection').find_elements_by_tag_name('strong')[3].text
        kf_lists = []
        butt = driver.find_element_by_xpath('//*[@id="root"]/div/div/div[2]/div/div[2]/div/div[1]/a[2]')
        butt.click()
        time.sleep(1)
        data = get_publish_date(driver)
        if data == 'nope': break
        for i in range(4):
            scroll_down(driver)
            try:
                driver.find_element_by_xpath(
                    f'//*[@id="root"]/div/div/div[2]/div/div[2]/div/div[2]/div/div[{str((i * 5) + 6)}]/button').click()
            except:
                try:
                    driver.find_element_by_xpath(
                        f'//*[@id="root"]/div/div/div[2]/div/div[2]/div/div[2]/div/div[{str((i * 5) + 6 - 5)}]/button').click()
                except:
                    driver.find_element_by_xpath(
                        f'//*[@id="root"]/div/div/div[2]/div/div[2]/div/div[2]/div/div[{str((i * 5) + 6 - 10)}]/button').click()

            time.sleep(15)
        html = get_html_sel(driver)
        soup = BeautifulSoup(html, 'lxml')
        items2 = soup.find_all('div', 'ui segment')
        for item2 in items2:
            stav1 = item2.find('h3', 'ui header').text
            stav = stav1 + ' ' + item2.find('div', 'active-tips-score').find('span').text
            kf = item2.find('strong').text
            kf_lists.append(float(kf[kf.find('@') + 1:].strip()))
            try:
                bookmacker = item2.find('div', 'grey-bg lose').find('a').get('href')
            except:
                try:
                    bookmacker = item2.find('div', 'grey-bg win').find('a').get('href')
                except:
                    bookmacker = 'not given'
            publish_date = item2.find('span', 'smaller grey').text
            link_stav = item2.find('h3', 'ui header').get('href')
            try:
                result = item2.find_elements_by_class_name('div', 'grey-bg lose')
            except:
                result = 'Win'
            else:
                result = 'Lose'
            end = {'Ставка': stav.strip(), 'КФ': kf,
                   'Букмекер': bookmacker.strip(),
                   'Время публикации': publish_date.strip(),
                   'Ссылка на пост': link_stav, 'Результат': result.strip()}
            spisok.append(end)

        middle_kf = sum(kf_lists) / len(kf_lists)
        main_data['Имя Каппера'].append(name_capper)
        main_data['Сcылка на канал'].append(link_capper)
        main_data['Количество ставок'].append(col_stav.replace('\n', ''))
        main_data['Roi(Yield на некоторых сайтах) %'].append(roi_yield)
        main_data['Profit'].append(profit)
        main_data['Ср. Кф за все ставки'].append(middle_kf)
        main_data['Winrate(%)'].append(winrate)
        main_data['Ставки'].append(spisok)
def long():
    driver = get_links()
    parse_data(driver)
    save_data('Bet2Earn.xlsx', main_data)


long()
