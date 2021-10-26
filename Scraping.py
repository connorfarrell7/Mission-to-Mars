from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

### Scrape the title and summary of the first story
def mars_news(browser):

    url = 'https://redplanetscience.com'
    browser.visit(url)
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    html = browser.html
    news_soup = soup(html, 'html.parser')
    slide_elem = news_soup.select_one('div.list_text')

    try:
        slide_elem.find('div', class_='content_title')
        
        news_title = slide_elem.find('div', class_='content_title').get_text()
        
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except:
        return None, None
    
    return news_title, news_p

### Scrape the featured
def featured_image(browser):

    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    
    except:
        return None

    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

### Scrape the "Mars Facts" table and place into a Pandas DataFrame
def mars_facts():

    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    
    except:
        return None

    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    return df.to_html()

browser.quit()