from main_functions import *

url = 'https://tipstrr.com/football'
main_data = {'Имя Каппера': [], 'Сcылка на канал': [], 'Количество ставок': [], 'Roi(Yield на некоторых сайтах) %': [],
             'Profit': [], 'Ср. Кф за все ставки': [], 'Winrate(%)': [], 'Ставки': []}
pre_link_list = []
pre_link_list1 = []
links_list = []
sports_list = []


def get_pre_links():
    driver = create_driver()
    driver.get(url)
    time.sleep(3)
    html = get_html_sel(driver)
    soup = BeautifulSoup(html, 'lxml')
    links = soup.find_all('li')
    for linking in links:
        try:
            pre_link_list.append('https://tipstrr.com ' + linking.find('a').get('href'))
        except:
            print('i skip that shit')
    pre_link_list.pop(0)
    pre_link_list1.extend(pre_link_list[:17])
    return driver


def get_links(driver):
    pre_link_list1 = ['https://tipstrr.com/football']
    for pre_link in pre_link_list1:
        driver.get(pre_link)
        for i in range(6):
            scroll_down2(driver)
    thebutton = driver.find_element_by_xpath(
        '//*[@id="page-content"]/div[1]/ng-component/discover-table/div[2]/div/div/div[3]/button')
    thebutton.click()
    while thebutton != None:
        scroll_down2(driver)
        time.sleep(10)
        try:
            thebutton = driver.find_element_by_xpath(
                '//*[@id="page-content"]/div[1]/ng-component/discover-table/div[2]/div/div/div[3]/button')
            thebutton.click()
        except:
            break
        time.sleep(4)
    extra_html = get_html_sel(driver)
    extra_soup = BeautifulSoup(extra_html, 'lxml')
    items = extra_soup.find('ul', 'divide-y divide-grey-light-2').find_all('li')
    print(items)
    for item in items:
        try:
            link = 'https://tipstrr.com' + item.find('a').get('href')
        except:
            print()
        else:
            print(link)
            links_list.append(link)
            sports = item.find('span',
                               'absolute w-6 h-6 p-1 bg-white border rounded-full -bottom-1 -right-1 lg:w-8 lg:h-8 border-grey-light-3').find(
                'img').get('alt')
            sports_list.append(sports)


def get_publish_date(driver):
    list_years = ['2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010',
                  '2009', '2008', '2007', '2006']
    months = ['Aug', 'Jul', 'Jun', 'May', 'Apr', 'Feb', 'Jan']
    data = 'yes'
    last_page = driver.current_url
    driver.get(last_page + '/results')
    time.sleep(3)
    driver.find_element_by_xpath(
        '//*[@id="page-content"]/div[1]/ng-component/tipster-header/nav/ul/li[5]/a').click()
    time.sleep(3)
    html4 = get_html_sel(driver)
    soup4 = BeautifulSoup(html4, 'lxml')
    publish_date = soup4.find_all('local-date')[1].text
    check = soup4.find('div', 'result--bet').find_all(text=True)
    if 'Trixie' in check: data = 'nope'
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
    return data


def parse_data(driver):
    links_list = ['https://tipstrr.com/tipster/soccerrafa']
    sports_list = ['Football']
    for linkk, sport in zip(links_list, sports_list):
        spisok = []
        driver.get(linkk)
        data = get_publish_date(driver)
        if data == 'nope': break
        driver.get(linkk)
        html = get_html_sel(driver)
        soup = BeautifulSoup(html, 'lxml')
        col_stav = soup.find('p', 'lead')
        needed_text = col_stav.find_all(text=True)[2]
        print(needed_text)
        number = needed_text[needed_text.find('across') + len('across'):needed_text.find(sport)].strip()
        print(number)
        number = 501  # delete
        if int(number) <= 500: break
        name_capper = driver.find_element_by_class_name('text-primary-dark').text
        print(name_capper)
        link_capper = linkk
        col_stavv = number
        roi_yield = driver.find_element_by_class_name('splash--stats').find_elements_by_tag_name('li')[
            1].find_element_by_tag_name('dt').text
        print(roi_yield)
        profit = driver.find_element_by_class_name('splash--stats').find_elements_by_tag_name('li')[
            5].find_element_by_tag_name('dt').find_element_by_tag_name('span').text
        print(profit)
        middle_kf = driver.find_element_by_class_name('splash--stats').find_elements_by_tag_name('li')[
            4].find_element_by_tag_name('odds').find_element_by_tag_name('span').text
        print(middle_kf)
        winrate = driver.find_element_by_class_name('splash--stats').find_elements_by_tag_name('li')[
            3].find_element_by_tag_name('dl').find_element_by_tag_name('dt').text
        print(winrate)
        driver.get(driver.current_url + '/results')
        time.sleep(4)
        for i in range(4):
            scroll_down2(driver)
            time.sleep(0.5)
            driver.find_element_by_xpath('//*[@id="page-content"]/div[1]/ng-component/div/div/button').click()
            time.sleep(3)
        html5 = get_html_sel(driver)
        soup5 = BeautifulSoup(html5, 'lxml')
        items2 = soup5.find_all('div', 'result result--listing')
        print(bool(items2))
        for i in range(10):
            scroll_up(driver)
        a = 1
        for item2 in items2:
            stav1 = item2.find('div', 'result--bet').find('h6').find_next('a').text
            print(stav1)
            try:
                stav2 = item2.find('div',
                                   'result--bet').find(
                    'h5').find_all(text=True)
                print(stav2)
            except:
                pass
            else:
                stav = stav1 + ' ' + stav2[0] + ' ' + stav2[-1]
                print(stav)
                kf = item2.find('span', 'odds odds-static no-padding').get('data-odds')
                print(kf)
                link_post = 'https://tipstrr.com' + item2.find('div', 'result--bet').find('h6').find_next('a').get(
                    'href')
                print(link_post)
                result = item2.find('span', 'result--wl-text').text
                print(result)
                bookmacker = item2.find('div', 'result--bookie').find('img').get('alt')
                print(bookmacker)
                publish_date = item2.find('local-date').text
                print(publish_date)

                end = {'Ставка': stav.strip(), 'КФ': kf,
                       'Букмекер': bookmacker.strip(),
                       'Время публикации': publish_date.strip(),
                       'Ссылка на пост': link_post, 'Результат': result.strip()}
                spisok.append(end)

        main_data['Имя Каппера'].append(name_capper)
        main_data['Сcылка на канал'].append(link_capper)
        main_data['Количество ставок'].append(col_stavv)
        main_data['Roi(Yield на некоторых сайтах) %'].append(roi_yield)
        main_data['Profit'].append(profit)
        main_data['Ср. Кф за все ставки'].append(middle_kf)
        main_data['Winrate(%)'].append(winrate)
        main_data['Ставки'].append(spisok)


def long():
    driver = get_pre_links()
    get_links(driver)
    parse_data(driver)
    save_data('Tipster.xlsx', main_data)


long()
