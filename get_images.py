import requests
import ast
import os
import re
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from utils import save_content_to_file, makedir, read_file

def download_images(save_path, target_search, chromepath):

    driver = webdriver.Chrome(chromepath)
    url = 'http://www.google.com/search?q=' + target_search + '&tbm=isch'
    driver.get(url)
    while True:
        current_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if current_height == new_height:
            try:
                driver.find_element_by_xpath("//input[@type='button']").click()
            except:
                break
    images = driver.find_elements_by_tag_name('img')

    idx = 1

    for img in images:
        src = img.get_attribute('src')
        if not src:
            src = img.get_attribute('data-src')
        if src.startswith('https://'):
            try:
                response = requests.get(src)
                if response.status_code == 200:
                    imagename = save_path + 'image_' + str(idx) + '.jpg'
                    save_content_to_file(response.content, imagename, 'wb')
                    idx += 1
            except:
                continue

    soup = str(BeautifulSoup(driver.page_source, 'html.parser'))
    driver.quit()

    images_jpg = re.findall(r'\[\"https:(.*?).jpg', soup)
    images_jpeg = re.findall(r'\[\"https:(.*?).jpeg', soup)

    for img in images_jpg:
        imageurl = 'https:' + img + '.jpg'
        try:
            response = requests.get(imageurl)
            if response.status_code == 200:
                imagename = save_path + 'image_' + str(idx) + '.jpg'
                save_content_to_file(response.content, imagename, 'wb')
                idx += 1
        except:
            continue

    for img in images_jpeg:
        imageurl = 'https:' + img + '.jpeg'
        try:
            response = requests.get(imageurl)
            if response.status_code == 200:
                imagename = save_path + 'image_' + str(idx) + '.jpg'
                save_content_to_file(response.content, imagename, 'wb')
                idx += 1
        except:
            continue

if __name__ == '__main__':

    chromepath = os.getcwd() + '/chromedriver'
    path = str(input("Escull 'Bolets Comestibles','Bolets Verinosos' o 'altres':"))
    save_directory = 'Imatges_Bolets/' + path.title().replace(' ', '_') + '/'
    file_name ='Noms/' + path.lower().replace(' ', '_') +'.txt'

    while path != 'Bolets Comestibles' and path != 'Bolets Verinosos':
        if path.lower() != 'altres':
            print("El valor d'entrada no està contemplat entre les opcions disponibles")
        answer = str(input("Vols utilitzar una ruta alternativa per carregar els noms dels bolets i guardar les imatges? (si/no)")).lower()
        if answer == 'si':
            save_directory = str(input("Directori on es guardaran les imatges:"))
            file_name = str(input("Ruta per accedir als noms dels bolets:"))
            break
        elif answer == 'no':
            path = str(input("Escull 'Bolets Comestibles', 'Bolets Verinosos' o 'altres':"))
            save_directory = 'Imatges_Bolets/' + path.title().replace(' ', '_') + '/'
            file_name ='Noms/' + path.lower().replace('', '_') +'.txt'
            continue
        else:
            raise ValueError("El valor d'entrada és incorrecte")

    contents = read_file(file_name, "r")
    list_of_names = ast.literal_eval(contents).keys()

    for name in list_of_names:
        save_location = save_directory + name + '/'
        makedir(save_location)
        download_images(save_location, name, chromepath)