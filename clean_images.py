import os
from PIL import Image, ImageChops

def remove_replicates(path):
    images = [path+file for file in os.listdir(path) if os.path.isfile(path+file)]
    idx = 0
    while idx < len(images):
        slide = 1
        while slide < len(images) - idx:
            if not ImageChops.difference(Image.open(images[idx]), Image.open(images[idx+slide])).getbbox():
                os.remove(images[idx+slide])
                del images[idx+slide]
                slide -= 1
            slide += 1
        idx += 1

def main(species):
    for item in species:
        remove_replicates(item)

if name == __main__:
    path = str(input("Quines imatges vols netejar? 'Bolets Comestibles', 'Bolets Verinosos' o 'altres':"))
    if path != 'Bolets Comestibles' and path != 'Bolets Verinosos':
        path = str(input("Directori a netejar:"))
    else:
        species = ['Images/' + path + '/' + file + '/' for file in os.listdir('Images/' + path + '/')]

    main(species)