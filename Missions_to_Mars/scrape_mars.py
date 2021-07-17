from splinter import browser
from bs4 import BeautifulSoup
from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager

def scrape_info():
    driver = webdriver.Chrome(ChromeDriverManager().install())

    url = "https://redplanetscience.com/"

    driver.get(url) 

    time.sleep(1)

    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')
    results = soup.find_all("div", class_="list_text")
    
    news_title = soup.find_all("div", class_="content_title")
    news_title = news_title[0].text

    news_p = soup.find_all("div", class_ = "article_teaser_body")
    news_p = news_p[0].text

## JPL Mars Space Images - Featured Image

    url_image = "https://spaceimages-mars.com/"
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url_image) 

    html_image= driver.page_source
    soup_image = BeautifulSoup(html_image, "html.parser")

    images = soup_image.find_all("a", class_="showimg fancybox-thumbs")
    href = images[0]["href"]
    featured_image_url = f"https://spaceimages-mars.com/{href}"

## Mars Fact
    url_table = "https://galaxyfacts-mars.com/"
    tables = pd.read_html(url_table)

    df = tables[0]
    df.columns = ["Description", 'Mars', "Earth"]
    df.set_index("Description")

    html_table = df.to_html()
    html_table.replace('\n', '')
    df.to_html('table.html')

## Mars Hemispheres
    url_hem = "https://marshemispheres.com/"
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url_hem) 
    url_hem= driver.page_source
    soup_hem = BeautifulSoup(url_hem, "html.parser")

    collapsible_results = soup_hem.find_all("div", class_="collapsible results")

    titles = collapsible_results[0].find_all("h3")

    # Loop through to find Hemisphere title
    hem_titles = []

    for title in titles:
        hem_titles.append(title.text)
    hem_titles    

    image_results = collapsible_results[0].find_all("a")
    images = image_results[0].find("img")["src"]

    # Loop through the web page to find url for each full image
    image_url = []
    for full_image in image_results:
        if (full_image.img):
        
            img_url = "https://marshemispheres.com/" + full_image["href"]
            image_url.append(img_url)
    image_url

    # Loop through the URL above to find the full image url
    full_image_url = []
    for img_url in image_url:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(img_url) 
        link = driver.page_source
        soup_image = BeautifulSoup(link, "html.parser")
        full_image = soup_image.find_all("img", class_="wide-image")
        image_link = full_image[0]["src"]
        img_link = "https://marshemispheres.com/" + image_link
        full_image_url.append(img_link)
        
    full_image_url   

    # Append the dictionary with the image url string and the hemisphere title to a list
    hemisphere_image_urls = []
    hem_image = zip(hem_titles, full_image_url)

    for hem_titles, full_image_url in hem_image:
        dict = {}
        dict["title"] = hem_titles
        dict["img_url"] = full_image_url
        hemisphere_image_urls.append(dict)
    
    hemisphere_image_urls

## store scraped data into a dictionary
    mars_info = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": featured_image_url,
        "mars_facts": mars_table,
        "mars_hemispheres": hemisphere_image_urls
    }

# Close the browser after scraping
    driver.quit()

# Return results
    return mars_info
