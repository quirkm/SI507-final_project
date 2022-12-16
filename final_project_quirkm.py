import requests
from bs4 import BeautifulSoup
import time
import shutil
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
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

class Fungi:
    def __init__(self):
        self.name = "Unknown"
        self.fam_tree =  "Unknown"
        self.distribution =  "Unknown"
        self.taxonomy =  "Unknown"
        self.etymology =  "Unknown"
        self.culinary =  "Unknown"
        self.toxicity =  "Unknown"
        self.mythology =  "Unknown"
        self.psychoactivity =  "Unknown"
        self.url =  "Unknown"

def get_species_details(fungi_url, fungi_name):

    response = make_url_request_using_cache(fungi_url, CACHE_DICT)
    soup = BeautifulSoup(response, 'html.parser')

    selected_fungi = Fungi()
    selected_fungi.name = fungi_name
    selected_fungi.url = fungi_url

    selected_species_info = soup.find('div', class_='container') # the smallest class that contains all the information about the specified species
    species_tree_info = selected_species_info.findAll('p')
    fam_tree = species_tree_info[1].text

    selected_fungi.fam_tree = fam_tree

    headers_and_content = selected_species_info.findAll(['h2','p','h3'])

    for i in range(len(headers_and_content)):
        if headers_and_content[i].text.lower() == 'distribution':
            distribution = ''
            for k in range(6):
                if headers_and_content[i+1+k].name == 'p':
                    distribution += headers_and_content[i+1+k].text

            selected_fungi.distribution = distribution
            # print(distribution)

        elif headers_and_content[i].text.lower() == 'taxonomic history':
            taxonomy = ''
            for k in range(5):
                if headers_and_content[i+1+k].name == 'p':
                    taxonomy += headers_and_content[i+1+k].text

            selected_fungi.taxonomy = taxonomy


        elif headers_and_content[i].text.lower() == 'etymology':
            etymology = ''
            for k in range(5):
                if headers_and_content[i+1+k].name == 'p':
                    etymology += headers_and_content[i+1+k].text

            selected_fungi.etymology = etymology

        elif headers_and_content[i].text.lower() == 'toxicity':
            toxicity = ''
            for k in range(12):
                if headers_and_content[i+1+k].name == 'p':
                    toxicity += headers_and_content[i+1+k].text

            selected_fungi.toxicity = toxicity

        elif headers_and_content[i].text.lower() == 'mythology':
            mythology = ''
            for k in range(12):
                if headers_and_content[i+1+k].name == 'p':
                    mythology += headers_and_content[i+1+k].text
            selected_fungi.mythology = mythology

        elif 'psychoactive' in headers_and_content[i].text.lower():
            psychoactivity = ''
            for k in range(3):
                if headers_and_content[i+1+k].name == 'p':
                    psychoactivity += headers_and_content[i+1+k].text
            selected_fungi.psychoactivity = psychoactivity

        elif headers_and_content[i].text.lower() == 'culinary notes':
            culinary = ''
            for k in range(4):
                if headers_and_content[i+1+k].name == 'p':
                    culinary += headers_and_content[i+1+k].text
            selected_fungi.culinary = culinary

    return selected_fungi

def choose_nav(selected_fungi):
    choose = input(f"You have selected to learn more about {selected_fungi.name}. \n \
    Your navigation options to learn more about this fungi are as follows: 'Family Tree', 'Distribution' , ' Etymology', 'Taxonomic History', 'Psychoactivity', 'Mythology', 'Toxicity', 'Culinary Notes'. \n \
        Please now type one of the above options here. ")

    if choose.lower().strip() == 'distribution':
        print('\n')
        print(f'{selected_fungi.name} - Distribution')
        print(selected_fungi.distribution)
        print('\n')
    elif choose.lower().strip() == 'etymology':
        print('\n')
        print(f'{selected_fungi.name} - Etymology')
        print(selected_fungi.etymology)
        print('\n')
    elif choose.lower().strip() == 'taxonomic history':
        print('\n')
        print(f'{selected_fungi.name} - Taxonmic History')
        print(selected_fungi.taxonomy)
        print('\n')
    elif choose.lower().strip() == 'psychoactivity':
        print('\n')
        print(f'{selected_fungi.name} - Psychoactivity')
        print(selected_fungi.psychoactivity)
        print('\n')
    elif choose.lower().strip() == 'mythology':
        print('\n')
        print(f'{selected_fungi.name} - Mythology')
        print(selected_fungi.mythology)
        print('\n')
    elif choose.lower().strip() == 'toxicity':
        print('\n')
        print(f'{selected_fungi.name} - Toxicity')
        print(selected_fungi.toxicity)
        print('\n')
    elif choose.lower().strip() == 'culinary notes':
        print('\n')
        print(f'{selected_fungi.name} - Culinary Notes')
        print(selected_fungi.culinary)
        print('\n')
    elif choose.lower().strip() == 'family tree':
        print('\n')
        print(f'{selected_fungi.name} - Family Tree')
        print(selected_fungi.fam_tree)
        print('\n')

    choose_again = input(f"If you'd like to choose another category, type 'again'. Otherwise, type 'exit' to leave this species' page. ")

    if choose_again.lower().strip() == 'again':
        return choose_nav(selected_fungi)




# Load the cache, save in global variable
CACHE_DICT = load_cache()

def get_fungi_info(): # extracting main fungi page info to traverse through

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

    fungi_select = input(f"Please enter the number of a Fungi Family to learn more about the family and its members. Or type 'exit' to quit the program. ")

    if fungi_select.lower().strip() == 'exit':
        print(f"Thanks for participating! Bye!")
        return

    selected_fam_url = tuple(fungi_fam_url_dict.items())[int(fungi_select)-1][1]
    selected_fam_name = tuple(fungi_fam_url_dict.items())[int(fungi_select)-1][0]

    def get_fam_info(selected_fam_url, selected_fam_name):

        # get requested family page
        response = make_url_request_using_cache(selected_fam_url, CACHE_DICT)
        soup = BeautifulSoup(response, 'html.parser')

        fungi_family_child = soup.find('div', class_='container') # the smallest class that contains all the information about the families of fungi
        fungi_family_info = fungi_family_child.findAll('p')

        gen_fam_info = input(f"If you'd like to learn more about the {selected_fam_name} family in general, type 'Y'. Otherwise type 'N' to select a species within the family to learn more about it. Or type 'restart' to go back to the beginning. ")

        fungi_species = soup.find('div', class_='clearfix') # the smallest class that contains all the information about the species of selected fungi
        fungi_species_divs = fungi_species.findAll('div', recursive=False)

        fungi_species_url_dict = {}
        # extract family names & put in dict with urls
        for fungi_species in fungi_species_divs:
            # extract the course details URL
            fungi_species_tag = fungi_species.find('a')
            # print(fungi_species_tag)
            fungi_species_path = fungi_species_tag['href']
            fungi_img = fungi_species.find('img')
            fungi_species_img_alt = fungi_img['alt']
            # print(fungi_species_img_alt)
            fungi_species_details_url = BASE_URL + fungi_species_path
            fungi_species_url_dict[fungi_species_img_alt.strip()] = fungi_species_details_url


        if gen_fam_info.lower() == 'y':
            print('\n')
            print(f"General info about {selected_fam_name}")
            stop_index = 0
            for i in range(len(fungi_family_info)):
                if 'top of page' in fungi_family_info[i].text.lower():
                    stop_index = len(fungi_family_info) - i
                    break
            for line in fungi_family_info[:-stop_index]:
                print(line.text)
            print('\n')
            continue_to_species = input(f"If you'd like to select a species now within this family, type 'Y'. Otherwise, type 'restart' to go back to the beginning or 'exit' to quit the program. ")
            if continue_to_species.lower().strip() == 'y':
                print(f"Fungi Species in the {selected_fam_name} Family")
                for i, key in enumerate(fungi_species_url_dict.keys()):
                    print(f"{i+1}. {key}")
                select_species = input(f"Please enter the number of a species above to learn more about the fungus. " )
                selected_species_name = tuple(fungi_species_url_dict.items())[int(select_species)-1][0]
                selected_species_url = tuple(fungi_species_url_dict.items())[int(select_species)-1][1]
                selected_species = get_species_details(selected_species_url, selected_species_name)
                choose_nav(selected_species)

                another_species = input(f"If you'd like to go back to the beginning and choose another fungi family, type 'restart'. If you'd like to go back to select another species in this family, type 'species'. Otherwise, type 'exit' to quit. ")

                if another_species.lower().strip() == 'restart':
                    return get_fungi_info()
                elif another_species.lower().strip() == 'species':
                    return get_fam_info(selected_fam_url, selected_fam_name)
                else:
                    print(f"Thanks for participating! Bye!")

            elif continue_to_species.lower().strip() == 'restart':
                return get_fungi_info()
            else:
                print(f"Thanks for participating! Bye!")

        elif gen_fam_info.lower() == 'n':
            print('\n')
            print(f"Fungi Species in the {selected_fam_name} Family")
            for i, key in enumerate(fungi_species_url_dict.keys()): ## ADD TRY EXCEPT CLAUSES?? ugh
                print(f"{i+1}. {key}")
            select_species = input(f"Please enter the number of a species above to learn more about the fungus. If you'd like to go back to the beginning, type 'restart'. " )
            if select_species.lower().strip() == 'restart':
                return get_fungi_info()
            else:
                selected_species_name = tuple(fungi_species_url_dict.items())[int(select_species)-1][0]
                selected_species_url =tuple(fungi_species_url_dict.items())[int(select_species)-1][1]
                selected_species = get_species_details(selected_species_url, selected_species_name)
                choose_nav(selected_species)

            another_species = input(f"If you'd like to go back to the beginning and choose another fungi family, type 'restart'. If you'd like to go back to select another species in this family, type 'species'. Otherwise, type 'exit' to quit. ")

            if another_species.lower().strip() == 'restart':
                return get_fungi_info()
            elif another_species.lower().strip() == 'species':
                return get_fam_info(selected_fam_url, selected_fam_name)
            else:
                print(f"Thanks for participating! Bye!")

        elif gen_fam_info.lower().strip() == 'restart':
            return get_fungi_info()

    return get_fam_info(selected_fam_url, selected_fam_name)



print(f"Welcome! \n Within this program you will be able to select different families and species of fungi to learn more about them. ")
begin = input(f"Are you ready to begin? (y/n) ")

if begin.lower().strip() == 'y':
    get_fungi_info()
else:
    print(f"No problem. See you next time! ")

