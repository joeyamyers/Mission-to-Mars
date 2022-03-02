#!/usr/bin/env python
# coding: utf-8

# Import Splinter , BeautifulSoup, pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# set the executable path
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# ### automate visit to Mars news site

def mars_news(browser):

    # assign url and instruct the browser to visit it
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    # search for elements w combo of div tag and list_text attribute
    # tell browser to wait 1 sec before searching for components just in case it takes a bit to load pages
    browser.is_element_present_by_css('div.list_text', wait_time=1)


    # set up html parser
    # html object
    html = browser.html
    news_soup = soup(html, 'html.parser')
    

     # Add try/except for error handling
    try:
         # parent element - slide_elem holds a large chunk of info for first article: date, title, teaser
        slide_elem = news_soup.select_one('div.list_text')

        # search the parent element to find the first `a` tag and save it as `news_title`
        # .get_text() returns us only text and none of the extra html
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Search the parent element to find the teaser text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None


    return news_title, news_p


# ### Featured Images

def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)


    # Find and click the full image button - want to click 2nd button
    full_image_elem = browser.find_by_tag('button')[1]
    # splinter will click the image to view its fill size
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # tell BS to look inside <img /> tag for an image w class of fancybox-image
    # This is where the image we want lives- use .get('src') pulls the link to the image
    img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    

    return img_url_rel, img_url


# ### Mars Facts

# scrape entire table w pd function .read_html()
# func specifically looks for and returns tables found in html specify 1st table w [0]
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df
# convert df back into html
df.to_html()

# end automated browser session
browser.quit()