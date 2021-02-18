import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from utils import save_content_to_file

def get_soup_text(link, parser = 'lxml'):
    
    """ CAT: retorna un 'soup element' a partir d'un localitzador uniforme de recursos (sigles URL en anglès)
        EN: returns a 'soup element' from a URL
        input arguments: URL (string), parser (string) """
    
    return BeautifulSoup(requests.get(link).text, parser)

def get_names(bs_element, replacements = []):
    
    """ CAT: retorna 
    """
    
    names = [name.text for name in bs_element]
    for char in replacements:
        names = [name.replace(char,'') for name in names]
    return names

def find_items(soup, tag_id, tag_especific, case='m'):
    if case == 'M':
        return soup.find(*tag_id).findAll(*tag_especific)
    return soup.find(*tag_id).find_all(*tag_especific)

def get_latin_names(names):
    names_latin = []
    for bolet in names:
        link = 'https://www.google.com/search?q=' + bolet
        soup = get_soup_text(link)
        try:
            find_name = soup.find_all('a', href=True, text=re.compile("Wikipedia"))
            latin_name = re.findall(r'/wiki/(.*?)&', str(find_name[0]))[0].replace('_',' ')
        except:
            response = soup.find_all('a')
            new_item = next(str(item) for item in response if 'wiki' in str(item))
            [new_name] = re.findall('wikipedia.org/wiki/(.*?)&amp', new_item)
            try:
                new_link = "https://ca.wikipedia.org/wiki/" + new_name
                new_soup = get_soup_text(new_link)
                latin_name = new_soup.find("div", {"class": 'mw-parser-output'}).find('i').text
            except AttributeError:
                new_link = "https://es.wikipedia.org/wiki/" + new_name
                new_soup = get_soup_text(new_link)
                latin_name = new_soup.find("div", {"class": 'mw-parser-output'}).find('i').text
            except:
                continue
        names_latin.append(latin_name)
    return names_latin
        
def main():
    df = pd.read_pickle('Noms/url comestibles')

    bolets_comestibles = []

    for idx in df.index:
        soup = get_soup_text(df['url'][idx])
        text = find_items(soup, df['tag id'][idx], df['tag especific'][idx], case=df['grafia'][idx])
        names = get_names(text, replacements=df['replace'][idx])
        bolets_comestibles += names
        bolets_comestibles = list(set(bolets_comestibles) | set(names))

    bolets_comestibles += ['Bolet de tinta','Mollerons','Cogomella']

    excepcions_catala = ast.literal_eval(read_file('Noms/excepcions comestibles catala.txt', 'r'))
    excepcions_llati = ast.literal_eval(read_file('Noms/excepcions comestibles llati.txt', 'r'))

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
    main()