import os
from PIL import Image, ImageChops

def remove_replicates(path):
    images = [path+file for file in os.listdir(path) if os.path.isfile(path+file)]
    idx = 0
    while idx < len(images):
        check_replicates = 1
        while check_replicates < len(images) - idx:
            if not ImageChops.difference(Image.open(images[idx]), Image.open(images[idx+check_replicates])).getbbox():
                os.remove(images[idx+check_replicates])
                del images[idx+check_replicates]
                check_replicates -= 1
            check_replicates += 1
        idx += 1

def main(species):
    for item in species:
        remove_replicates(item)
    
if name == __main__:
    path = str(input("Quines imatges vols netejar? 'Bolets Comestibles', 'Bolets Verinosos' o 'altres':"))
    if path != 'Bolets Comestibles' and path != 'Bolets Verinosos':
        path = str(input("Directori a netejar:"))
    else:t
        species = ['Images/' + path + '/' + file + '/' for file in os.listdir('Images/' + path + '/')]
    
    main(species)
