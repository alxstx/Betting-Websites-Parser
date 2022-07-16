from main_functions import *

url = 'https://blogabet.com/tipsters'
# links = []
main_data = {'Имя Каппера': [], 'Сcылка на канал': [], 'Количество ставок': [], 'Roi(Yield на некоторых сайтах) %': [],
             'Profit': [], 'Ср. Кф за все ставки': [], 'Winrate(%)': [], 'Ставки': []}

newf_lists = []
links = []
newff_lists = []

def get_links():
    driver = create_driver()
    driver.get(url)
    driver.find_element_by_xpath('/html/body/div[4]/div[3]/div/div[2]/div/div/button').click()
    time.sleep(10)
    scroll_down(driver)
    time.sleep(1.5)
    thebutton = driver.find_element_by_xpath('//*[@id="_loadMore"]/a')
    while thebutton != None:
        time.sleep(20)
        scroll_down(driver)
        time.sleep(0.5)
        try:
            thebutton = driver.find_element_by_xpath('//*[@id="_loadMore"]/a')
        except:
            time.sleep(5)
            scroll_down(driver)
            try:
                thebutton = driver.find_element_by_xpath('//*[@id="_loadMore"]/a')
            except:
                time.sleep(10)
                scroll_down(driver)
                thebutton = driver.find_element_by_xpath('//*[@id="_loadMore"]/a')
        try:
            thebutton.click()
        except:
            break
    lists = driver.find_elements_by_class_name('img-md')
    f_lists = driver.find_elements_by_class_name("number")
    namber = 2
    for f, fl in enumerate(f_lists):
        f = f + 1
        if f == namber:
            newf_lists.append(fl)
        if f % 6 == 0:
            namber += 6
    for l, newf in zip(lists, newf_lists):
        if int(newf.text) >= 500:
            links.append(l.get_attribute('href'))
            newff_lists.append(newf.text)

    return driver


def get_publish_date(driver):
    list_years = ['2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010',
                  '2009', '2008', '2007', '2006']
    months = ['Aug','Jul','Jun','May','Apr','Feb','Jan']
    data = 'yes'
    html = get_html_sel(driver)
    soup = BeautifulSoup(html, 'lxml')
    publish_date = soup.find('small', 'text-muted').find_all(text=True)[-1]
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
    """links = ['https://sabobic.blogabet.com/']  # test
    newff_lists = [1200]  # test"""
    for link, newff in zip(links, newff_lists):
        spisok = []
        driver.get(link)
        driver.find_element_by_xpath('/html/body/div[4]/div[3]/div/div[2]/div/div/button').click()
        time.sleep(2)
        kf_lists = []
        winrate_lists = []
        data = get_publish_date(driver)
        if data == 'nope': break
        name_capper = driver.find_element_by_class_name('enable-tooltip').get_attribute('data-original-title')
        link_channel = link
        amount_stavok = newff
        roi_yield = driver.find_element_by_xpath('//*[@id="header-yield"]').text
        profit = driver.find_element_by_xpath('//*[@id="header-profit"]').text
        for i in range(4):
            scroll_down(driver)
            time.sleep(10)
            driver.find_element_by_xpath('//*[@id="last_item"]/a').click()
            time.sleep(3)
        html = get_html_sel(driver)
        soup = BeautifulSoup(html, "lxml")
        items = soup.find_all('div', class_='feed-pick-title')
        for number, item in enumerate(items):
            stav = item.find('div', 'pick-line').find_all(text=True)[0]
            kf = item.find('span', 'feed-odd').text
            bookmacker = item.find('small', 'text-muted').find_all(text=True)[2]
            publish_date = item.find('small', 'text-muted').find_all(text=True)[-1]
            link_stav = item.find('h3').find_next('a').get('href')
            result1 = item.find('div', 'labels').find_all('span')
            result = result1[-2].text

            if '+' in result:
                winrate_lists.append('1')
            else:
                winrate_lists.append('0')

            kf_lists.append(float(kf))
            end = {'Ставка': stav.replace('\n', '').replace('@', '').strip(), 'КФ': kf,
                   'Букмекер': bookmacker.replace('\n', '').replace('/', '').strip(),
                   'Время публикации': publish_date.strip(),
                   'Ссылка на пост': link_stav, 'Результат': result.strip()}
            spisok.append(end)

        middle_kf = sum(kf_lists) / len(kf_lists)
        count_wins = winrate_lists.count('1')
        winrate = count_wins / len(winrate_lists) * 100

        main_data['Имя Каппера'].append(name_capper)
        main_data['Сcылка на канал'].append(link_channel)
        main_data['Количество ставок'].append(amount_stavok)
        main_data['Roi(Yield на некоторых сайтах) %'].append(roi_yield)
        main_data['Profit'].append(profit)
        main_data['Ср. Кф за все ставки'].append(middle_kf)
        main_data['Winrate(%)'].append(winrate)
        main_data['Ставки'].append(spisok)

def long():
    driver = get_links()
    parse_data(driver)
    save_data('Blogabet.xlsx',main_data)

long()