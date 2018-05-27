# params
search_term = "quantum"
search_limit = 150
outut_dir = "E:\\downloads_ch9\\"

base_Url_child_pages_with_videos = ("https://channel9.msdn.com/Search?term=" + str(search_term) + "#ch9Search&pubDate=all&lang-en=en&pageSize=" + str(search_limit))
xpath_find_all_child_pages = "//ul[@class='resultsList']//div[@class='secondary']//header//h3//a"
xpath_find_video_url = "//div[@class='download']//a[contains(text(), 'MP4') or contains(text(), 'WMV') or contains(text(), 'AVI')]"

chromium_path = "E:\\Tools\\selenium_drivers\\chromedriver.exe"
time_sleep_seconds = 5




import os  
from selenium import webdriver  
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import os
import time
import urllib.request




def GetLinks(_url, _xpath, _chromium_path, _sleep_time):
    xchrome_options = Options()  
    xchrome_options.add_argument("--headless")  
    browser = webdriver.Chrome(executable_path=chromium_path, chrome_options=xchrome_options)
    browser.get(_url)
    time.sleep(time_sleep_seconds)

    links_to_download = [] 
    all_link_base = browser.find_elements_by_xpath(_xpath)
    for link in all_link_base:
        links_to_download.append(link.get_attribute("href"))

    return links_to_download





# get all child pages that constains a video
child_pages_with_videos = GetLinks(_url = base_Url_child_pages_with_videos, _xpath = xpath_find_all_child_pages, _chromium_path = chromium_path, _sleep_time = time_sleep_seconds)


videos_to_download = []
for link in child_pages_with_videos:
    
    # get best quality video that exists
    temp_video_size = 0
    temp_video_url = ""

    try:
        videos_urls = GetLinks(_url = link, _xpath = xpath_find_video_url, _chromium_path = chromium_path, _sleep_time = time_sleep_seconds)

        if len(videos_urls) > 0:

            for video_url in videos_urls:
                temp_current_video_size = urllib.request.urlopen(video_url).length
                if (temp_current_video_size > temp_video_size):
                    temp_video_size = temp_current_video_size
                    temp_video_url = video_url

            videos_to_download.append(link + "  :   " + temp_video_url)
        else: 
            videos_to_download.append(link + "  :   " + "no videos avaliable")
    except:
        pass
        videos_to_download.append(link + "  :   " + "video download error")



# save all video urls to download to file
videos_to_download_to_save = map(lambda x: x + '\n', videos_to_download)
output_file_name = outut_dir + "myoutputfile.txt"
outF = open(output_file_name, "w")
outF.writelines(list(videos_to_download_to_save))
outF.close()



