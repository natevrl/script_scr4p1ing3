import requests
from bs4 import BeautifulSoup
import re


url = 'HIDED'
header_info = {'cookie': 'HIDED'}
session = requests.Session()
with_cookie = session.get(url, headers=header_info)
soup = BeautifulSoup(with_cookie.text, 'html.parser')

def scrap_liens():
    parse_HIDED = soup.findAll('div', {'class':"course-listing"})
    liens_HIDEDs = []
    for lien in parse_HIDED:
        a = lien.find('a')
        lien = url + a['href'][1:]
        liens_HIDEDs.append(lien)
    return liens_HIDEDs


def scrap_videos():
    liens_videos = []
    for lien_HIDED in scrap_liens():
        r = session.get(lien_HIDED, headers=header_info)
        soup = BeautifulSoup(r.text, 'html.parser')
        parse_videos = soup.findAll('a', {'class':'item'})
        for video in parse_videos:
            a = video['href']
            lien = url + a[1:]
            liens_videos.append(lien)
    return liens_videos



def scrap_code_secret():
    list_code_secret = []
    for lien in scrap_videos():
        r = session.get(lien, headers=header_info)
        soup = BeautifulSoup(r.text, 'html.parser')
        if soup.find('div', {'class': 'HIDED'}) is not None:
            script = soup.find('div', {'class': 'HIDED'}).find('div', {'class':"attachment-HIDED-player stillSnap=false HIDED_embed videoFoam=true"}).get('id')[7:]
            contacts_link = 'HIDED' + script
            list_code_secret.append(contacts_link)
    return list_code_secret


def regex_lien_final():
    nb_video = 0
    print("demarrage du telechagement...")
    for lien in scrap_code_secret()[326:625]:
        r = session.get(lien, headers=header_info)
        soup = BeautifulSoup(r.text, 'html.parser')
        script = soup.findAll('script')[4]
        regex = r"https?:\/\/[a-zA-Z0-9-_\.\/]+"
        titre_video = soup.find('title').text.replace(" ", "_")
        chemin = 'HIDED' + titre_video
        lien_final = re.findall(regex, str(script))[0]
        nb_video += 1
        progress = str(nb_video) + "/624"
        print("Downloading file numbers {} : {}".format(progress, titre_video))
        r = session.get(lien_final)
        with open(chemin, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)
        print("{} downloaded!\n".format(progress))
    print('tout est download !')
    return


regex_lien_final()
