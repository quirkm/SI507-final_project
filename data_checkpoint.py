import requests
from bs4 import BeautifulSoup
import time
import shutil
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import json

BASE_URL = 'https://www.first-nature.com/fungi/'
ID_GUIDE_PATH = '~id-guide.php'
CACHE_FILE_NAME = 'fungi_cache.json'
CACHE_DICT = {}

def load_cache():
    try:
        cache_file = open(CACHE_FILE_NAME, 'r')
        cache_file_contents = cache_file.read()
        cache = json.loads(cache_file_contents)
        cache_file.close()
    except:
        cache = {}
    return cache


def save_cache(cache):
    cache_file = open(CACHE_FILE_NAME, 'w')
    contents_to_write = json.dumps(cache)
    cache_file.write(contents_to_write)
    cache_file.close()


def make_url_request_using_cache(url, cache):
    if (url in cache.keys()): # the url is our unique key
        print("Using cache")
        return cache[url]
    else:
        print("Fetching")
        time.sleep(1)
        response = requests.get(url)
        cache[url] = response.text
        save_cache(cache)
        return cache[url]

def extract_img(fungi_div, href_link):
    ## extracting images of all the fungi families
    fungi_fam_img = fungi_div.find('img')
    fungi_img_src = fungi_fam_img.attrs['src']
    full_img_url = BASE_URL + fungi_img_src
    img_request = requests.get(full_img_url, stream=True)
    filename = f"{href_link[1:-4]}.jpg"

    # Check image
    if img_request.status_code == 200:
        # Preventing the downloaded image’s size from being zero.
        img_request.raw.decode_content = True
        # Open a local file
        with open(filename,'wb') as f:
            shutil.copyfileobj(img_request.raw, f)
        print('Image successfully Downloaded: ',filename)
    else:
        print('Image Couldn\'t be retrieved')

def select_fungi_url():
    pass

# Load the cache, save in global variable
CACHE_DICT = load_cache()

## Make the soup for the whole fungi page
allFungi_page_url = BASE_URL + ID_GUIDE_PATH
url_text = make_url_request_using_cache(allFungi_page_url, CACHE_DICT)
# response = requests.get(allFungi_page_url)
soup = BeautifulSoup(url_text, 'html.parser')
# print(url_text)

fungi_family_parent = soup.find('div', class_='clearfix') # the smallest class that contains all the information about the families of fungi
fungi_family_divs = fungi_family_parent.find_all('div', recursive=False)

# print(fungi_family_divs)

fungi_fam_url_dict = {}
# extract family names & put in dict with urls
for fungi_fam in fungi_family_divs:
    # extract the course details URL
    fungi_fam_tag = fungi_fam.find('a')
    fungi_fam_path = fungi_fam_tag['href']
    fungi_fam_details_url = BASE_URL + fungi_fam_path
    fungi_fam_url_dict[fungi_fam_tag.text.strip()] = fungi_fam_details_url

### SELECT A FAMILY ###
print("Fungus Families")
for i, key in enumerate(fungi_fam_url_dict.keys()):
    print(f"{i+1}. {key}")

fungi_select = input(f"Please enter the number of a Fungi Family to learn more about its members. ")
selected_fam_url = tuple(fungi_fam_url_dict.items())[int(fungi_select)-1][1]

# get requested family page
response = requests.get(selected_fam_url)
soup = BeautifulSoup(response.text, 'html.parser')

fungi_family_child = soup.find('div', class_='container') # the smallest class that contains all the information about the families of fungi
fungi_family_paragraph = fungi_family_child.findAll('p')
print(fungi_family_paragraph[4].text) #figuring out the best way to get general text about the family - changes across fams

