# Dependencies
import time
import pandas as pd
import requests as req
from bs4 import BeautifulSoup as bs
from splinter import Browser


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    # Visit url for NASA Mars News 
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, "html.parser")

    # Extract article title and paragraph text
    article = soup.find("div", class_='list_text')
    news_title = article.find("div", class_="content_title").text
    news_p = article.find("div", class_ ="article_teaser_body").text

    # Mars Image
    # Visit url for Mars Image
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)

    # You need to click through to get the the proper HTML to parse and get the image
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)

    browser.click_link_by_partial_text('more info')
    time.sleep(5)

    # Now you can parse HTML with BS 
    html = browser.html

    image_soup = bs(html, 'html.parser')

    # Scrape the url to extract the image 
    image_class = image_soup.find('figure', class_="lede")
    image_href = image_class.a['href']
    featured_image_url = (f'https://www.jpl.nasa.gov/{image_href}')

    #Twitter 

    # Mars Facts

    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    html = browser.html

    # use Pandas to scrape and create table
    table = pd.read_html(facts_url)
    mars_facts = table[0]

    # rename columns
    mars_facts.columns = ["Description", "Value"]

    # set Description to index
    mars_facts.set_index("Description")

    mars_facts_html = mars_facts.to_html(class= "table table-striped")

    # Mars Hemispheres

    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html

    # BS 
    soup = bs(html, "html.parser")

    hemisphere_image_urls = []

    results = soup.find("div", class_ = "result-list" )
    hemispheres = results.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup = bs(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_image_urls.append({"title": title, "img_url": image_url})

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts": mars_facts,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data

if __name__ == '__main__':
    scrape()