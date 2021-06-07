from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

def scrape():
    #----NASA MARS NEWS----
    #Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #Visit mars.nasa.gov
    nasa_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(nasa_url)
    time.sleep(2)

    #Create Beautiful Soup object to scrape most recent article into soup
    html = browser.html
    soup = bs(html, 'html.parser')

    #Get the most recent article title and description
    articles = soup.find_all('div', class_='list_text')[0]
    news_title = articles.find(class_='content_title').text
    news_p = articles.find(class_='article_teaser_body').text

    #Store scraped data in dicitonary
    mars_dict = {
        "news_title": news_title,
        "news_p": news_p
    }

    #Shutdown splinter instance
    browser.quit()

    #----FEATURED MARS IMAGE----
    #Setup splinter instance
    browser = Browser('chrome', **executable_path, headless=False)

    #Visit data-class-jpl website
    JPL_url= 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(JPL_url)

    #Create Beautiful Soup object to scrape most recent article into soup
    html = browser.html
    soup = bs(html, 'html.parser')

    #Get the featured image url
    feature_image = soup.find('div', class_='floating_text_area')
    a = feature_image.find('a')
    href = a['href']
    featured_image_url = (f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{href}')

    #Add feature image URL to mars.dict dictionary
    mars_dict['featured_image_url'] = featured_image_url

    #Shutdown splinter instance
    browser.quit()

    #----MARS FACTS----
    #URL to scrape tables containing Mars data
    facts_url = 'https://space-facts.com/mars/'

    #Scrape tables from facts_url using pandas
    tables = pd.read_html(facts_url)

    #Convert first table to pandas dataframe
    mars_df = tables[0]

    #Rename columns of dataframe and reset index to Characteristic column
    mars_df.rename(columns={ 0: 'Characteristic', 1: "Mars"}, inplace=True)
    mars_df.set_index('Characteristic', inplace=True)

    #Generate html table
    mars_html_table = mars_df.to_html()

    #Add to mars_dict
    mars_dict['mars_facts'] = mars_html_table

    #----MARS HEMIS----
    #Setup splinter instance
    browser = Browser('chrome', **executable_path, headless=False)

    #Visit astrogeology.usgs.gov
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)

    #Create Beautiful Soup object to scrape most recent article into soup
    html = browser.html
    soup = bs(html, 'html.parser')
    results = soup.find_all('div', class_='description')

    #Create list to store hemi URLs
    mars_hemi_image_urls = []

    #Loop through each of the four hemisphere pages
    for hemis in results:
        hemi = hemis.find('h3').text
        browser.click_link_by_partial_text(hemi)
        html = browser.html
        soup = bs(html, 'html.parser')
        hemi_images = soup.find('div', class_='downloads')
        hemi_a = hemi_images.find('a')
        hemi_href = hemi_a['href']
        hemi_dict = {
            'title' : hemi,
            'img_url' : hemi_href
        }
        mars_hemi_image_urls.append(hemi_dict)
        browser.back()
    
    #Append hemi image urls to mars_dict
    mars_dict['mars_hemi_image_urls'] = mars_hemi_image_urls

    #Shutdown splinter instance
    browser.quit()

    return mars_dict