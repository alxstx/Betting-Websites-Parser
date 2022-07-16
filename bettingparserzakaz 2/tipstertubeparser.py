from main_functions import *

url = 'https://tipstertube.com/tipsters/?f-minimum=25&f-active=1'
main_data = {'Имя Каппера': [], 'Сcылка на канал': [], 'Количество ставок': [], 'Roi(Yield на некоторых сайтах) %': [],
             'Profit': [], 'Ср. Кф за все ставки': [], 'Winrate(%)': [], 'Ставки': []}

links = []
number_list = []


def get_links():
    driver = create_driver()
    driver.get(url)
    time.sleep(5)
    scroll_down(driver)
    butt = driver.find_element_by_xpath('//*[@id="s-list1"]/div[2]/div[2]/div[2]/ul/li[2]/a')
    while butt != None:
        scroll_down(driver)
        items = driver.find_elements_by_tag_name('tr')
        items.pop(0)
        for item in items:
            try:
                link = item.find_elements_by_class_name('field-text')[
                    0].find_element_by_tag_name(
                    'a').get_attribute('href')
            except:
                link = 'There is no links'
            print(link)
            try:
                nambers = item.find_elements_by_class_name('field-text')[2].text
            except:
                nambers = 0
            print(nambers)
            if int(nambers) >= 500:
                links.append(link)
                number_list.append(nambers)
        try:
            butt = driver.find_element_by_xpath('//*[@id="s-list1"]/div[2]/div[2]/div[2]/ul/li[2]/a')
        except:
            break
        else:
            butt.click()
    return driver


def get_publish_date(driver):
    list_years = ['2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010',
                  '2009', '2008', '2007', '2006']
    months = ['Aug', 'Jul', 'Jun', 'May', 'Apr', 'Feb', 'Jan']
    data = 'yes'
    html_extra = get_html_sel(driver)
    extra_soup = BeautifulSoup(html_extra, 'lxml')
    publish_date = extra_soup.find('span','js-timeago').text
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
    links = ['https://tipstertube.com/profile/birbet']
    number_list = [501]
    for link, numba in zip(links, number_list):
        spisok = []
        driver.get(link)
        time.sleep(1.5)
        html = get_html_sel(driver)
        soup = BeautifulSoup(html, 'lxml')
        data = get_publish_date(driver)
        if data == 'nope':
            print('end')
            break
        name_capper = soup.find('div', 'ibox-content text-center').find_all(text=True)[5]
        print(name_capper)
        link_stav = link
        col_stav = numba
        roi_yield = soup.find_all('h3', 'no-margin')[3].text
        print(roi_yield)
        profit = soup.find_all('h3', 'no-margin')[5].text
        print(profit)
        middle_kf = soup.find_all('h3', 'no-margin')[8].text
        print(middle_kf)
        winrate = soup.find_all('h3', 'no-margin')[4].text
        print(winrate)
        for i in range(4):
            scroll_down(driver)
            driver.find_element_by_xpath('//*[@id="page-wrapper"]/div[5]/div/div/div[1]/div[2]/div/div/button').click()
            time.sleep(3)
        html2 = get_html_sel(driver)
        soup2 = BeautifulSoup(html2, 'lxml')
        items = soup2.find_all('div', 'row hidden-md hidden-lg screen-small')
        print(bool(items))
        for item in items:
            stav = item.find('strong', 'event').find('a').text + ' ' + item.find_all('div','col-xs-6 text-center')[-1].find_all(text=True)[2]
            print(stav)
            kf = item.find_all('div','col-xs-4 text-center')[-1].find_all(text=True)[-1]
            print(kf)
            bookmacker = item.find('div','col-xs-4 text-center post-pick-bookmaker').find_next('a').get('title')
            print(bookmacker)
            publish_date = item.find('span','js-timeago').text
            print(publish_date)
            link_post = 'https://tipstertube.com'+ item.find('strong', 'event').find('a').get('href')
            print(link_post)
            try:
                result = item.find('span','i-result result-lost')
            except:
                result = 'Win'
            else:
                result = 'Lose'
            print(result)
            end = {'Ставка': stav.strip().replace('\t','').replace('\n',''), 'КФ': kf.replace('\t','').replace('\n',''),
                   'Букмекер': bookmacker.strip(),
                   'Время публикации': publish_date.strip(),
                   'Ссылка на пост': link_post, 'Результат': result.strip()}
            spisok.append(end)
        main_data['Имя Каппера'].append(name_capper)
        main_data['Сcылка на канал'].append(link_stav)
        main_data['Количество ставок'].append(col_stav)
        main_data['Roi(Yield на некоторых сайтах) %'].append(roi_yield.strip())
        main_data['Profit'].append(profit.strip())
        main_data['Ср. Кф за все ставки'].append(middle_kf)
        main_data['Winrate(%)'].append(winrate.strip())
        main_data['Ставки'].append(spisok)


def long():
    driver = get_links()
    parse_data(driver)
    save_data('Tipstertube.xlsx', main_data)


long()
