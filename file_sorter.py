import argparse
import logging
from pathlib import Path
import re
from shutil import copyfile, rmtree
from threading import Thread


'''
WARNING: the sorting folder and the destination folder cannot be the same
'''

'''
python3 file_sorter.py --source -s folder
python3 file_sorter.py --output -o dist 
'''


EXTENSIONS = {
    'images': ['.jpeg', '.png', '.jpg', '.svg'],
    'video': ['.avi', '.mp4', '.mov', '.mkv'],
    'documents': ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'],
    'music': ['.mp3', '.ogg', '.wav', '.amr'],
    'archives': ['.zip', '.gz', '.tar']
}

CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'

TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {}

parser = argparse.ArgumentParser(description='App for sorting folder')

parser.add_argument('-s', '--source', help='Source folder', required=True)      
parser.add_argument('-o', '--output', default='dist')  

args = vars(parser.parse_args())
source = args.get('source')
output = args.get('output')


for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


def normalize(name: str) -> str:
    translate = name.translate(TRANS)
    translate = re.sub(r'\W', '_', translate)
    
    return translate


def get_categories(file:Path):

    extension = file.suffix.lower()
     
    for k, v in EXTENSIONS.items():

        if extension in v:
            return k
        
    return 'unknown'


def get_folders(path:Path):

    for el in path.iterdir():
        if el.is_dir():
            folders.append(el)
            get_folders(el)


def sort_file(path:Path):

    for el in path.iterdir():

        if el.is_file():

            category = get_categories(el)
            new_path = folder_destination / category
            try:
                new_path.mkdir(exist_ok=True, parents=True)
                file_stem = normalize(el.stem)
                copyfile(el, new_path.joinpath(f'{file_stem}{el.suffix}'))
            except OSError as e:
                logging.error(e)

    logging.debug('Files sorted')


if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')

    folder_for_sorting = Path(source)
    folder_destination = Path(output)

    folders = []
    folders.append(folder_for_sorting)

    get_folders(folder_for_sorting)
    
    threads = []
    
    for folder in folders:
        th = Thread(target=sort_file, args=(folder,))
        th.start()
        threads.append(th)

    [th.join() for th in threads]

    print('Now you can delete base folder')

    rmtree(folder_for_sorting)

    print('Finished work')

