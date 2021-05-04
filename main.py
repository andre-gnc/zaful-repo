import json
import random
import socket
import time
from pprint import pprint

import pandas as pandas
import urllib3
from bs4 import BeautifulSoup

import requests


def delay():
    sleep = random.randint(10, 20)  # Delay for 10 to 20 seconds. ====================================================
    print('Sleep:', sleep)  # =======================================================================================
    time.sleep(sleep)


def soup(sp_url, sp_parser, sp_head, sp_parmters, sp_proxy):
    response = requests.get(sp_url, headers=sp_head, params=sp_parmters, proxies=sp_proxy)
    print(response)  # =============================================================================================
    delay()

    if response.status_code == 200:
        sp_soup = BeautifulSoup(response.text, sp_parser)
    else:
        raise (socket.gaierror, urllib3.exceptions.NewConnectionError, urllib3.exceptions.MaxRetryError,
               requests.exceptions.ConnectionError)

    return sp_soup


def scraper(s_url):
    if scraper_testing is True:
        s_url = 'https://www.zaful.com/button-up-fleece-jean-jacket-puid_4749978.html?kuid=1007162'

    s_head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4389.128 Safari/537.36 OPR/75.0.3969.243'}

    try:  # Sometimes connection got error. So catch some exceptions.

        s_soup = soup(s_url, 'html.parser', s_head, None, None)
        # print(s_soup.prettify())  # ================================================================================
        # print(80 * '=')  # =========================================================================================

        s_json_tags = s_soup.find_all('script', {'type': 'application/ld+json'})[1].string  # Remember, string!
        s_json_data = json.loads(s_json_tags)

        # pprint(s_json_data)  # =====================================================================================
        # print('=' * 80)  # =========================================================================================

        try:
            title = s_json_data['name']
        except Exception:
            title = 'none'

        try:
            sku = s_json_data['sku']
        except Exception:
            sku = 'none'

        try:
            release_date = s_json_data['releaseDate']
        except Exception:
            release_date = 'none'

        try:
            price = s_json_data['offers']['price']
        except Exception:
            price = 'none'

        try:
            price_currency = s_json_data['offers']['priceCurrency']
        except Exception:
            price_currency = 'none'

        try:
            image = s_json_data['image']
        except Exception:
            image = 'none'

        try:
            material = s_json_data['material']
        except Exception:
            material = 'none'

        try:
            rating_value = s_json_data['review']['reviewRating']['ratingValue']
        except Exception:
            rating_value = 'none'

        print('Title:', title)
        print('SKU:', sku)
        print('Release Date:', release_date)
        print('Price:', price)
        print('Price Currency:', price_currency)
        print('Image:', image)
        print('Material:', material)
        print('Rating Value:', rating_value)

        return [title, sku, release_date, price, price_currency, image, material, rating_value]

    except (socket.gaierror, urllib3.exceptions.NewConnectionError, urllib3.exceptions.MaxRetryError,
            requests.exceptions.ConnectionError) as err:

        print('Error connecting:', err)
        return 'error'


def sample_urls():
    su_head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4389.128 Safari/537.36 OPR/75.0.3969.243'}

    su_entry_list = ['https://www.zaful.com/men-hoodies-sweatshirts-e_139/',
                     'https://www.zaful.com/men-shirts-e_138/']

    su_entry_urls = []
    try:  # Sometimes connection got error. So catch some exceptions.
        for su_cat_urls_cnt, su_cat_url in enumerate(su_entry_list):
            su_soup = soup(su_cat_url, 'html.parser', su_head, None, None)
            # print(su_soup.prettify())  # ===========================================================================
            # print(80 * '=')  # =====================================================================================

            su_entry_url_tags = su_soup.find_all('li', attrs={'class': 'js_proList_item logsss_event_ps'})
            for su_entry_url_tags_cnt, su_entry_url_tag in enumerate(su_entry_url_tags):
                su_entry_urls.append(su_entry_url_tag.find('a').get('href'))

        pprint(su_entry_urls)  # ===================================================================================
        print('Sample urls:', len(su_entry_urls))

        su_entry_urls_df = pandas.DataFrame(su_entry_urls)
        su_entry_urls_df = su_entry_urls_df.sample(frac=1)  # Make it random.
        su_entry_urls_df.to_csv('sample urls.csv', index=False)

    except (socket.gaierror, urllib3.exceptions.NewConnectionError, urllib3.exceptions.MaxRetryError,
            requests.exceptions.ConnectionError) as err:
        print('Error connecting:', err)
        return 'error'


def sample():
    sl_headers = ['Title', 'SKU', 'Release Date', 'Price', 'Price Currency', 'Image', 'Material', 'Rating Value']

    sl_entry_urls_df = pandas.read_csv('sample urls.csv')
    # pprint(sl_entry_urls_df) # =====================================================================================

    sl_df = pandas.DataFrame(columns=sl_headers)

    for cnt in range(1, len(sl_entry_urls_df) + 1):
        if cnt % team[1] == team[0]:
            sl_url = sl_entry_urls_df.iloc[cnt - 1]['0']
            sl_row = scraper(sl_url)

            if sl_row == 'error':
                break
            else:
                sl_series = pandas.Series(sl_row, index=sl_headers)
                sl_df = sl_df.append(sl_series, ignore_index=True)

                # Below: Counting, so that you can know which row is it.  # ==========================================
                print('The above is #' + str(cnt) + ' from ' + str(len(sl_entry_urls_df)) + ' entries.')
                print(80 * '=')  # =================================================================================

    pprint(sl_df)  # ===========================================================================================
    sl_df.to_csv(path_or_buf='sample ' + str(team[0]) + '.csv', index=False)


if __name__ == '__main__':
    scraper_testing = False
    team = [0, 12]  # [(#), (Total)]
    # scraper(None)
    # sample_urls()
    # sample()
