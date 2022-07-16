from main_functions import *

url_list = ['https://www.betadvisor.com/en/tipsters', 'https://www.betadvisor.com/en/freetipsters']
main_data = {'Имя Каппера': [], 'Сcылка на канал': [], 'Количество ставок': [], 'Roi(Yield на некоторых сайтах) %': [],
             'Profit': [], 'Ср. Кф за все ставки': [], 'Winrate(%)': [], 'Ставки': []}
links_list = []
number_list = []
middle_kff = []
winratee = []


def get_links():
    driver = create_driver()
    for url in url_list:
        driver.get(url)
        time.sleep(5)
        try:
            cookies = driver.find_element_by_xpath('//*[@id="cookiescript_accept"]')
            if cookies != None: cookies.click()
        except:
            time.sleep(3)

        scroll_down(driver)
        try:
            thebutton = driver.find_element_by_xpath('//*[@id="moretipsters"]')
        except:
            thebutton = driver.find_element_by_xpath('//*[@id="moretipstersfree"]')
        thebutton.click()
        time.sleep(5)
        while thebutton != None:
            scroll_down(driver)
            try:
                thebutton = driver.find_element_by_xpath('//*[@id="moretipsters"]')
            except:
                thebutton = driver.find_element_by_xpath('//*[@id="moretipstersfree"]')
            try:
                thebutton.click()
            except:
                break
            time.sleep(7)
        html = get_html_sel(driver)
        soup = BeautifulSoup(html, 'lxml')
        items = soup.find_all('div', 'grid-item add-collapse')
        print(bool(items))
        for item in items:
            link = 'https://www.betadvisor.com' + item.find('div',
                                                            'name-tipster').find('a').get('href')
            col_stavv = item.find('div', 'other-detail-listing').find_all('li')[2].find(
                'p').find('span').text
            if int(col_stavv) >= 500:
                links_list.append(link)
                number_list.append(col_stavv)
    return driver


def get_publish_data(driver):
    list_years = ['2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010',
                  '2009', '2008', '2007', '2006']
    months = ['Aug', 'Jul', 'Jun', 'May', 'Apr', 'Feb', 'Jan']
    data = 'yes'
    last_page = driver.current_url
    scroll_down2(driver)
    time.sleep(1)
    # driver.find_element_by_xpath('/html/body/main/div[7]/div/section/div[3]/a').click()
    html = get_html_sel(driver)
    soup = BeautifulSoup(html, 'lxml')
    publish_date = soup.find('td', 'date medium-txt').text
    print(publish_date)
    if '2021' in publish_date:
        for month in months:
            if month in publish_date:
                data = 'nope'
                break
    for year in list_years:
        if year in publish_date:
            data = 'nope'
            break
    driver.get(last_page)
    return data


def parse_data(driver):
    links_list = ['https://www.betadvisor.com/ru/tipsters/football/betaminic.html']
    number_list = ['2472']
    for linkk, namba in zip(links_list, number_list):
        spisok = []
        driver.get(linkk)
        try:
            cookies = driver.find_element_by_xpath('//*[@id="cookiescript_accept"]')
            if cookies != None: cookies.click()
        except:
            time.sleep(3)
        data = get_publish_data(driver)
        if data == 'nope': break
        scroll_up(driver)
        html2 = get_html_sel(driver)
        soup2 = BeautifulSoup(html2, 'lxml')
        name_capper = soup2.find('div', 'name-tipster').text
        print(name_capper)
        link_stav = linkk
        col_stav = namba
        roi_yield = soup2.find_all('div', 'bwaut001')[3].find('p', 'txt').text
        print(roi_yield)
        profit = soup2.find_all('div', 'bwaut001')[1].find('p', 'txt').text
        print(profit)
        for i in range(2):
            scroll_down2(driver)
        time.sleep(3)
        driver.find_element_by_xpath('/html/body/main/div[7]/div/section/div[4]/a').click()
        time.sleep(5)
        for i in range(4):
            if i != 0:
                driver.find_element_by_xpath('/html/body/main/div[7]/div/section/nav[2]/nav/ul/li[10]/a/span/i').click()
            for j in range(2):
                scroll_down2(driver)
            time.sleep(1.5)
            html = get_html_sel(driver)
            soup = BeautifulSoup(html, 'lxml')
            items2 = soup.find_all('tr')[65]
            print(items2)
            for item2 in items2:
                stav = item2.find('td', 'match').find('a').text + item2.find_all('td', 'selection medium-txt')[0]
                print(stav)
                kf = item2.find('td', 'medium-txt')[1].txt
                print(kf)
                bookmacker = item2.find_elements_by_class_name('selection medium-txt')[1].text
                print(bookmacker)
                publish_date = item2.find_element_by_class_name('date medium-txt').text
                print(publish_date)
                link_post = item2.find('td', 'match').find('a').get('href')
                print(link_post)
                result = item2.find('td', 'profit medium-txt profit_plus')
                print(result)
                middle_kff.append(kf)
                if '+' in result:
                    winratee.append('1')
                else:
                    winratee.append('0')
                end = {'Ставка': stav.strip(), 'КФ': kf,
                       'Букмекер': bookmacker.strip(),
                       'Время публикации': publish_date.strip(),
                       'Ссылка на пост': link_post, 'Результат': result.strip()}
                spisok.append(end)

        middle_kf = sum(middle_kff) / len(middle_kff)
        count_wins = winratee.count('1')
        print(count_wins)
        winrate = count_wins / len(winratee) * 100
        main_data['Имя Каппера'].append(name_capper)
        main_data['Сcылка на канал'].append(link_stav)
        main_data['Количество ставок'].append(col_stav)
        main_data['Roi(Yield на некоторых сайтах) %'].append(roi_yield)
        main_data['Profit'].append(profit)
        main_data['Ср. Кф за все ставки'].append(middle_kf)
        main_data['Winrate(%)'].append(winrate)
        main_data['Ставки'].append(spisok)

def long():
    driver = get_links()
    parse_data(driver)
    save_data('Betadvisor.xlsx', main_data)


long()