#!/usr/bin/env python
# coding: utf-8

# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

# func will intitialize browser, create a data dictionary, end the WebDriver and returned scraped data
def scrape_all():
   # Initiate headless driver for deployment
   executable_path = {'executable_path': ChromeDriverManager().install()}
   # headless = True, so we dont have to see the scraping in action
   browser = Browser('chrome', **executable_path, headless=True)

   # tells python we'll be using our mars_news() func to pull this data
   news_title, news_paragraph = mars_news(browser)

   # Dict runs all scraping functions I created and stores the results in dictionary
   data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemispheres(browser),
        "last_modified": dt.datetime.now()}

   # Stop webdriver and return data
   browser.quit()
   return data


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

    try:
        # tell BS to look inside <img /> tag for an image w class of fancybox-image
        # This is where the image we want lives- use .get('src') pulls the link to the image
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None
    
    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
   
    return img_url


# ### Mars Facts

def mars_facts():

    try:
        # try to scrape entire table w pd function .read_html()
        # read_html specifically looks for and returns tables found in html specify 1st table w [0]
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
      return None

    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    # convert df back into html format, add bootstrap
    return df.to_html(classes="table table-bordered")

# ### Hemispheres

def hemispheres(browser):
    # Use browser to visit the URL 
    url = 'https://marshemispheres.com/'

    browser.visit(url)

    # Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # create parent element that holds all links to full resolution images
    hemisphere_elem = browser.find_by_css('a.product-item img')

    # loop
    for i in range(len(hemisphere_elem)):
        hemispheres = {}
        
        # click on each icon to click thru to next page
        browser.find_by_css('a.product-item img')[i].click()
        
        # find img
        img = browser.find_by_text('Sample').first
        # add to dictionary
        hemispheres["img_url"] = img['href']
        
        
        # find title
        title = browser.find_by_css('h2.title').text
        # add to dictionary
        hemispheres["title"] = title
        
        # append to list
        hemisphere_image_urls.append(hemispheres)
    

        # browser back
        browser.back()


    # Quit the browser
    browser.quit()

    # return list of hemispheres dictionaries
    return hemisphere_image_urls




if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())