import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from utils import read_json_file, save_content_to_file, makedir

def get_soup_html(link, parser = 'lxml'):
    """ CAT: retorna un 'BeautifulSoup element' a partir d'un localitzador uniforme de recursos (sigles URL en anglès)
        EN: returns a BeautifulSoup element from a URL
        
        arguments: URL (str), parser (str)
        returns: BeautifulSoup element (bs4.BeautifulSoup)
    """
    
    return BeautifulSoup(requests.get(link).text, parser)


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


def get_latin_names(names):
    """ CAT: Troba els noms de les espècies en llatí a partir de la llista de noms en català
        EN: Finds the latin name of the species from a list of names in catalan
        
        arguments: List of names in catalan (list of str)
        returns: List of names in latin (list of str)
    """
    
    names_latin = []
    for bolet in names:
        # Afegim 'bolet' al final del nostre url de cerca
        link = 'https://www.google.com/search?q=' + bolet
        soup = BeautifulSoup(requests.get(link).text, parser)
        try:
            [find_name] = soup.find_all('a', href=True, text=re.compile("Wikipedia"))
            latin_name = re.findall(r'/wiki/(.*?)&', str(find_name))[0].replace('_',' ')
        except:
            response = soup.find_all('a')
            new_item = next(str(item) for item in response if 'wiki' in str(item))
            [new_name] = re.findall('wikipedia.org/wiki/(.*?)&amp', new_item)
            try:
                new_link = "https://ca.wikipedia.org/wiki/" + new_name
                new_soup = BeautifulSoup(requests.get(new_link).text, parser)
                latin_name = new_soup.find("div", {"class": 'mw-parser-output'}).find('i').text
            except AttributeError:
                latin_name = new_name.replace("_"," ")
            except:
                continue
        names_latin.append(latin_name)
    return names_latin


def main():
    
    #carreguem les url on 
    df = pd.read_pickle('Noms/url comestibles')

    bolets_comestibles = []

    for idx in df.index:
        soup = BeautifulSoup(requests.get(df['url'][idx]).text, parser)
        text = find_items(soup, df['tag id'][idx], df['tag especific'][idx], case=df['grafia'][idx])
        names = get_names(text, replacements=df['replace'][idx])
        bolets_comestibles += names
        bolets_comestibles = list(set(bolets_comestibles) | set(names))

    bolets_comestibles += ['Bolet de tinta','Mollerons','Cogomella']

    excepcions_catala = read_json_file('Noms/excepcions comestibles catala.txt', 'r')
    excepcions_llati = read_json_file('Noms/excepcions comestibles llati.txt', 'r')

    for nom in excepcions_catala:
        bolets_comestibles.remove(nom)

    cerca_bolets = [bolet + ' bolet' for bolet in bolets_comestibles]

    diferencies = ['Tòfona','Cigró','Gastronomia dels bolets','Llenega','Terfeziàcies']

    for nom in diferencies:
        excepcions_catala.remove(nom)

    noms_llati = get_latin_names(cerca_bolets)

    bolets_comestibles += excepcions_catala
    noms_llati += excepcions_llati

    bolets = dict(zip(noms_llati, bolets_comestibles))

    save_content_to_file(bolets,"Noms/bolets comestibles.txt","w")

if __name__ == '__main__':
    makedir("Noms/")
    main()