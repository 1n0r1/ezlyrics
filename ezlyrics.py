from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 
import questionary

class song:
    title = ""
    subtitle = ""
    url = ""

def search_url(a: str):
    URL = "https://genius.com/search?q="

    for i in range(len(a)):
        if a[i] == " ":
            URL = URL + "%20" 
        else:
            URL = URL + a[i]
    return URL

def generate_choices(list):
    re =[]
    for l in list:
        q = questionary.Choice(l.title + '\n' + "      " + l.subtitle, l.url)
        re.append(q)
    return re


def ask(list):
    k = questionary.select(
    "Select Song",
    choices = generate_choices(list)
    ).ask()
    return k

if __name__ == "__main__":
    to_search = questionary.text("Search lyrics: Enter song name/ artist").ask()
    searchURL = search_url(to_search)
    print(searchURL)

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)

    driver.get(searchURL)
    time.sleep(4)
    results = driver.find_elements_by_class_name("u-quarter_vertical_margins")
    songs = []
    for r in results[1:]:
        try:
            name = r.find_element_by_class_name("mini_card-title").text
            artist = r.find_element_by_class_name("mini_card-subtitle").text
            url = r.find_element_by_class_name("mini_card")
            s = song()
            s.title = name
            s.subtitle = artist
            s.url = url.get_attribute("href")
            songs.append(s)
        except:
            s = ""


    if (len(songs) == 0):
        print("No Result")
    else:
        lyrics_url = ask(songs)
        print(lyrics_url)

        d = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
        d.get(lyrics_url)
        d.implicitly_wait(30)
        lyrics = d.find_element_by_class_name("lyrics")
        print(lyrics.text)
        d.quit()

    driver.quit()

    

    
