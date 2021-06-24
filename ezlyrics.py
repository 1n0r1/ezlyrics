from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
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
        name = r.find_element_by_class_name("mini_card-title").text
        artist = r.find_element_by_class_name("mini_card-subtitle").text
        url = r.find_element_by_class_name("mini_card")
        s = song()
        s.title = name
        s.subtitle = artist
        s.url = url.get_attribute("href")
        songs.append(s)

    if (len(songs) == 0):
        print("No Result")
    else:
        lyrics_url = ask(songs)
        driver.get(lyrics_url)
        time.sleep(4)
        lyrics = driver.find_element_by_xpath('/html/body/routable-page/ng-outlet/song-page/div/div/div[2]/div[1]/div/defer-compile[1]/lyrics/div/div/section/p').text
        print(lyrics)

    

    
