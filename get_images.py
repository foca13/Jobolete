import requests
import ast
import os
import re
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from utils import save_content_to_file, makedir

def main(save_directory, input_list, chromepath):

    for i, name in enumerate(input_list):
        filename = save_directory + name
        makedir(filename)
        driver = webdriver.Chrome(chromepath)
        url = 'http://www.google.com/search?q=' + name + '&tbm=isch'
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
            imagename = filename + '/image_' + str(idx) + '.jpg'
            src = img.get_attribute('src')
            if not src:
                src = img.get_attribute('data-src')
            if src.startswith('https://'):
                try:
                    response = requests.get(src)
                    if response.status_code == 200:
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
            imagename = filename + '/image_' + str(idx) + '.jpg'
            try:
                response = requests.get(imageurl)
                if response.status_code == 200:
                    save_content_to_file(response.content, imagename, 'wb')
                    idx += 1
            except:
                continue

        for img in images_jpeg:
            imageurl = 'https:' + img + '.jpeg'
            imagename = filename + '/image_' + str(idx) + '.jpg'
            try:
                response = requests.get(imageurl)
                if response.status_code == 200:
                    save_content_to_file(response.content, imagename, 'wb')
                    idx += 1
            except:
                continue

if __name__ == '__main__':
    
    chromepath = os.getcwd() + '/chromedriver'
    path = str(input("Escull 'Bolets Comestibles','Bolets Verinosos' o 'altres':"))
    save_directory = 'Imatges/' + path + '/'
    file_name ='Noms/' + path.lower() +'.txt'

    while path != 'Bolets Comestibles' and path != 'Bolets Verinosos':
        if path.lower() != 'altres':
            print("El valor d'entrada no està contemplat entre les opcions predeterminades")
        answer = str(input("Vols utilitzar una ruta alternativa per carregar els noms dels bolets i guardar les imatges? (si/no)")).lower()
        if answer == 'si':
            save_directory = str(input("Directori on es guardaran les imatges:"))
            file_name = str(input("Ruta per accedir als noms dels bolets:"))
            break
        elif answer == 'no':
            path = str(input("Escull 'Bolets Comestibles', 'Bolets Verinosos' o 'altres':"))
            save_directory = 'Imatges/' + path + '/'
            file_name ='Noms/' + path.lower() +'.txt'
            continue
        else:
            raise ValueError("El valor d'entrada és incorrecte")
            
    contents = read_file(file_name, "r")
    
    input_data = ast.literal_eval(contents).keys()
    
    makedir(save_directory)

    main(save_directory, input_data, chromepath)