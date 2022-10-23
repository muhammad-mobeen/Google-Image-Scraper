import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  #..............
from selenium.webdriver.support import expected_conditions as EC    #................
import requests # to get image from the web
import shutil # to save it locally
from urllib.parse import urlparse
# from bs4 import BeautifulSoup
# import xlsxwriter
import time
# from selenium.webdriver.common.proxy import Proxy, ProxyType  #.................
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from msvcrt import getche, getch
import os

# url = "https://www.google.com/search?as_st=y&tbm=isch&as_q=&as_epq=badshahi+mosque&as_oq=&as_eq=&cr=&as_sitesearch=&safe=images&tbs=isz:lt,islt:xga"

def gen_driver():
    chrome_options = uc.ChromeOptions()
    chrome_options.headless = True
    # chrome_options.add_argument('--proxy-server=http://'+PROXY)
    driver = uc.Chrome(options=chrome_options)
    return driver

class ImagesScraper:
    def __init__(self):
        self.driver = gen_driver()
        self.search_querry = None

    def search(self):
        querry = self.search_querry.replace(" ", "+")

        # HD Quality
        # self.driver.get("https://www.google.com/search?as_st=y&tbm=isch&as_q=&as_epq={}&as_oq=&as_eq=&cr=&as_sitesearch=&safe=images&tbs=isz:lt,islt:xga".format(querry))
        
        # HD + Wide
        # self.driver.get("https://www.google.com/search?as_st=y&tbm=isch&as_q=&as_epq={}&as_oq=&as_eq=&cr=&as_sitesearch=&safe=images&tbs=isz:lt,islt:xga,iar:w".format(querry))
        
        # HD + Type:Photo
        self.driver.get("https://www.google.com/search?as_st=y&tbm=isch&as_q=&as_epq={}&as_oq=&as_eq=&cr=&as_sitesearch=&safe=images&tbs=isz:lt,islt:xga,itp:photo".format(querry))
        
        # HD + Wide + Type:Photo
        # self.driver.get("https://www.google.com/search?as_st=y&tbm=isch&as_q=&as_epq={}&as_oq=&as_eq=&cr=&as_sitesearch=&safe=images&tbs=isz:lt,islt:xga,itp:photo,iar:w".format(querry))


    def fetch_image_urls(self, quantity):
        # imgurle = self.driver.find_element_by_xpath('//*[@id="islrg"]/div[1]/div[%s]/a[1]/div[1]/img'%(str(indx)))
        # driver.find_elements(By.CSS_SELECTOR, '#__ZONE__main > div > div > div.main-categories.lohp-row.max-width-container > ul > li > a')
        imgurls = []
        for i in range(1,quantity+1):
            img_card = self.driver.find_element(By.XPATH, '//*[@id="islrg"]/div[1]/div[%s]/a[1]/div[1]/img'%(str(i)))
            img_card.click()
            time.sleep(6)
            popup_class = self.driver.find_elements(By.CLASS_NAME, 'n3VNCb')
            for popup in popup_class:
                imgurl = popup.get_attribute("src")
                if(("http" in  imgurl) and (not "encrypted" in imgurl)):
                    imgurls.append(imgurl)
                    print("[{}] Fetched Image url: {}".format(i,imgurl))
        return(imgurls)

    def dowload_images(self, imgurls):
        # Creates a new folder to save the images. If already exists, Overwrites it.
        images_dir = 'Images'
        if os.path.exists(images_dir):
            shutil.rmtree(images_dir)
        os.makedirs(images_dir)

        downloaded_images = []

        for i, image_url in enumerate(imgurls,1):
            #extact filename without extension from URL
            extract_url = urlparse(image_url)
           
            ## Set up the image URL and filename
            # filename = os.path.basename(extract_url.path)
            file_name, file_extension = os.path.splitext(os.path.basename(extract_url.path))
            if file_extension:
                filename = self.search_querry + " " + str(i) + file_extension
            else:
                filename = self.search_querry + " " + str(i) + ".jpg"

            # if similar name exists, don't overwrite please
            # if filename in downloaded_images:
            #     filename = str(i) + filename
            # else:
            #     downloaded_images.append(filename)

            # Open the url image, set stream to True, this will return the stream content.
            r = requests.get(image_url, stream = True)

            # Check if the image was retrieved successfully
            if r.status_code == 200:
                # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
                r.raw.decode_content = True
                
                # Open a local file with wb ( write binary ) permission.
                save_image_dir = os.path.join(os.getcwd(), os.path.join(images_dir, filename))
                with open(save_image_dir,'wb') as f:
                    shutil.copyfileobj(r.raw, f)
                    
                print('[{}] Image sucessfully Downloaded: {}'.format(i, filename))
            else:
                print('[{}] Image Couldn\'t be retreived: {}'.format(i, image_url))

 
if __name__ == "__main__":
    scrapeman = ImagesScraper()
    print("Enter the search term: ", end="")
    scrapeman.search_querry = input()
    scrapeman.search()
    imgurls = scrapeman.fetch_image_urls(8)
    # print(imgurls)
    scrapeman.dowload_images(imgurls)
    # search_querry.replace(" ", "+")
    # driver = gen_driver()
    # driver.get("https://www.google.com/search?as_st=y&tbm=isch&as_q=&as_epq={}&as_oq=&as_eq=&cr=&as_sitesearch=&safe=images&tbs=isz:lt,islt:xga".format(search_querry))
    