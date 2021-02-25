import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from utils import read_json_file, save_content_to_file, makedir


def find_items(soup, tag_id, tag_especific, case='m'):
    """ CAT: troba el contingut d'etiquetes' específiques d'un 'BeautifulSoup element'
        EN: finds the content of specific tags of a 'BeautifulSoup element'
        
        arguments: BeautifulSoup element (bs4.BeautifulSoup), main tag (str), specific tag 
                   (str, uppercase or lowercase search: 'm' or 'M'. Default: 'm', lowercase)
        returns: Set of contents from the target tags (bs4.element.ResultSet)
    """
    
    if case == 'M':
        return soup.find(*tag_id).findAll(*tag_especific)
    return soup.find(*tag_id).find_all(*tag_especific)


def get_names(bs_element, replacements = []):
    """ CAT: transforma un BeautifulSoup Result Set a una llista de strings
        EN: transforms a BeatifulSoup Result Set to a list of strings
        
        arguments: BeautifulSoup element (bs4.element.ResultSet), characters to replace (if any) (list of str)
        returns: mushroom names (list of str)
    """
    
    names = [name.text for name in bs_element]
    for char in replacements:
        names = [name.replace(char,'') for name in names]
    return names


def get_latin_names(names):
    """ CAT: Troba els noms de les espècies en llatí a partir de la llista de noms en català
        EN: Finds the latin name of the species from a list of names in catalan
        
        arguments: List of names in catalan (list of str)
        returns: List of names in latin (list of str)
    """
    
    names_latin = []
    for bolet in names:
        link = 'https://www.google.com/search?q=' + bolet
        soup = BeautifulSoup(requests.get(link).text, 'lxml')
        try:
            [find_name] = soup.find_all('a', href=True, text=re.compile("Wikipedia"))
            latin_name = re.findall(r'/wiki/(.*?)&', str(find_name))[0].replace('_',' ')
        except:
            response = soup.find_all('a')
            new_item = next(str(item) for item in response if 'wiki' in str(item))
            [new_name] = re.findall('wikipedia.org/wiki/(.*?)&amp', new_item)
            try:
                new_link = "https://ca.wikipedia.org/wiki/" + new_name
                new_soup = BeautifulSoup(requests.get(new_link).text, 'lxml')
                latin_name = new_soup.find("div", {"class": 'mw-parser-output'}).find('i').text
            except AttributeError:
                latin_name = new_name.replace("_"," ")
        names_latin.append(latin_name)
    print('Cerca de noms en llatí completada')
    return names_latin


def main():
    
    # CAT: carreguem el dataframe amb les url i tota la informació necessària per trobar els noms dels bolets
    # EN: we load the dataframe with the urls and all the information needed to find the names of the mushrooms
    df = pd.read_pickle('Noms/url_comestibles')

    bolets_comestibles = []

    for idx in df.index:
        soup = BeautifulSoup(requests.get(df['url'][idx]).text, 'lxml')
        text = find_items(soup, df['tag id'][idx], df['tag especific'][idx], case=df['grafia'][idx])
        names = get_names(text, replacements=df['replace'][idx])
        bolets_comestibles = list(set(bolets_comestibles) | set(names))

    bolets_comestibles += ['Bolet de tinta','Mollerons','Cogomella']

    excepcions_catala = read_json_file('Noms/excepcions_comestibles_catala.txt', 'r')
    excepcions_llati = read_json_file('Noms/excepcions_comestibles_llati.txt', 'r')

    bolets_comestibles = list(set(bolets_comestibles).difference(set(excepcions_catala)))
        
    # CAT: afegim la paraula 'bolet' al final de cada nom per facilitar la cerca a google. Per exemple, els bolets
    # 'Camperol' o 'Coliflor' són més fàcils de trobar si cerquem 'Camperol bolet' o 'Colifor bolet'. També es
    # podria afegir directament dins la funció get_latin_names
    # EN: we add the word 'bolet' (mushroom) at the end of each name to facilitate the google search. For example,
    # it is easier to find 'Camperol bolet' or 'Coliflor bolet' than 'Camperol' (Peasant) or 'Coliflor' (Cauliflower).
    # This could also be done inside the get_latin_names function
    cerca_bolets = [bolet + ' bolet' for bolet in bolets_comestibles]

    # aquests noms els traiem definitivament
    # we remove these names
    diferencies = ['Tòfona','Cigró','Gastronomia dels bolets','Llenega','Terfeziàcies']

    excepcions_catala = list(set(excepcions_catala).difference(set(diferencies)))

    # busquem els noms en llatí
    # we search for the names in latin
    noms_llati = get_latin_names(cerca_bolets)

    bolets_comestibles += excepcions_catala
    noms_llati += excepcions_llati

    bolets = dict(zip(noms_llati, bolets_comestibles))

    # guardem el diccionari final com una string en un arxiu .txt
    # we save the final dictionary as a string in a .txt file
    save_content_to_file(str(bolets),"Noms/bolets_comestibles.txt","w")

if __name__ == '__main__':
    makedir("Noms/")
    main()