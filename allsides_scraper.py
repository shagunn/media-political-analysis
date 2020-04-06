from bs4 import BeautifulSoup
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd


def scrape_allsides(urls, names, pgdowns):

    browser = webdriver.Safari()

    for idx, url in enumerate(urls):
        print('Scraping ' + names[idx])

        print('Getting data...  ')

        # get data
        browser.get(url)
        time.sleep(1)

        # addressing infinite scroll ... can probably be made faster but it works
        elem = browser.find_element_by_tag_name("body")
        no_of_pagedowns = pgdowns[idx]

        while no_of_pagedowns:
            elem.send_keys(Keys.PAGE_DOWN)
            time.sleep(2.0)
            no_of_pagedowns-=1

        # test code (without scroll)
        # r = requests.get(url)
        # soup = BeautifulSoup(r.content, 'html.parser')

        # parse data
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        print('Parsing data...  ')
        rows = soup.select('tbody tr')

        data_dict = {}
        name = []
        allsides_url = []
        bias = []
        agree = []
        disagree = []
        agree_ratio = []
        agree_desc = []

        for row in rows:
            name.append(row.select_one('.source-title').text.strip())
            allsides_url.append('https://www.allsides.com' + row.select_one('.source-title a')['href'])
            bias.append(row.select_one('.views-field-field-bias-image a')['href'].split('/')[-1])
            agree.append(int(row.select_one('.agree').text))
            disagree.append(int(row.select_one('.disagree').text))
            agree_ratio.append(agree[-1] / (disagree[-1]+0.00000001))  ## add some noise
            try:
                agree_desc.append(row.select_one('.hidden-xs').text.strip())
            except:
                agree_desc.append('NA')

        data_dict['name'] = name
        data_dict['url_as'] = allsides_url
        data_dict['bias_as'] = bias
        data_dict['agree_as'] = agree
        data_dict['disagree_as'] = disagree
        data_dict['agree_ratio_as'] = agree_ratio
        data_dict['agree_desc_as'] = agree_desc


        df = pd.DataFrame(data_dict)
        df.to_csv('data/AllSides/AllSides_' + names[idx] + '.csv', index=False)
        print('Saving csv...  ')
        print(' ')

        # time.sleep(10)
    browser.quit()

# urls - for capturing not rated
# urls = ['https://www.allsides.com/media-bias/media-bias-ratings?field_featured_bias_rating_value=All&field_news_source_type_tid%5B2%5D=2&field_news_bias_nid_1%5B1%5D=1&field_news_bias_nid_1%5B2%5D=2&field_news_bias_nid_1%5B3%5D=3&field_news_bias_nid_1%5B4%5D=4&title=',
#         'https://www.allsides.com/media-bias/media-bias-ratings?field_featured_bias_rating_value=All&field_news_source_type_tid%5B3%5D=3&field_news_bias_nid_1%5B1%5D=1&field_news_bias_nid_1%5B2%5D=2&field_news_bias_nid_1%5B3%5D=3&field_news_bias_nid_1%5B4%5D=4&title=',
#         'https://www.allsides.com/media-bias/media-bias-ratings?field_featured_bias_rating_value=All&field_news_source_type_tid%5B4%5D=4&field_news_bias_nid_1%5B1%5D=1&field_news_bias_nid_1%5B2%5D=2&field_news_bias_nid_1%5B3%5D=3&field_news_bias_nid_1%5B4%5D=4&title=']
# pagedowns = [120, 8, 4]
print("new3")

# urls = ['https://www.allsides.com/media-bias/media-bias-ratings?field_featured_bias_rating_value=All&field_news_source_type_tid%5B2%5D=2&field_news_bias_nid_1%5B1%5D=1&field_news_bias_nid_1%5B2%5D=2&field_news_bias_nid_1%5B3%5D=3&title=',
#         'https://www.allsides.com/media-bias/media-bias-ratings?field_featured_bias_rating_value=All&field_news_source_type_tid%5B3%5D=3&field_news_bias_nid_1%5B1%5D=1&field_news_bias_nid_1%5B2%5D=2&field_news_bias_nid_1%5B3%5D=3&title=',
#         'https://www.allsides.com/media-bias/media-bias-ratings?field_featured_bias_rating_value=All&field_news_source_type_tid%5B4%5D=4&field_news_bias_nid_1%5B1%5D=1&field_news_bias_nid_1%5B2%5D=2&field_news_bias_nid_1%5B3%5D=3&title=']
#
# names = ['News', 'Think_Tank_Policy_Group', 'Reference']
# pagedowns = [37, 5, 3]

# urls = ['https://www.allsides.com/media-bias/media-bias-ratings?field_featured_bias_rating_value=All&field_news_source_type_tid%5B2%5D=2&field_news_bias_nid_1%5B1%5D=1&field_news_bias_nid_1%5B2%5D=2&field_news_bias_nid_1%5B3%5D=3&title=',
#         'https://www.allsides.com/media-bias/media-bias-ratings?field_featured_bias_rating_value=All&field_news_source_type_tid%5B3%5D=3&field_news_bias_nid_1%5B1%5D=1&field_news_bias_nid_1%5B2%5D=2&field_news_bias_nid_1%5B3%5D=3&title=',
#         'https://www.allsides.com/media-bias/media-bias-ratings?field_featured_bias_rating_value=All&field_news_source_type_tid%5B4%5D=4&field_news_bias_nid_1%5B1%5D=1&field_news_bias_nid_1%5B2%5D=2&field_news_bias_nid_1%5B3%5D=3&title=']
#
# names = ['News', 'Think_Tank_Policy_Group', 'Reference']
# pagedowns = [37, 5, 3]

urls = ['https://www.allsides.com/media-bias/media-bias-ratings']
names = ['FeaturedNews']
pagedowns = [9]
print("uo")
scrape_allsides(urls, names, pagedowns)
