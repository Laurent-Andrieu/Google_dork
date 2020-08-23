import json
import os
import urllib.request

import requests

# Directories
USER = os.getlogin()
PATH = f'C:/Users/{USER}/Downloads/'
DEST_PATH = f'C:/Users/{USER}/PycharmProjects/'
# API
ENGINE_ID = ''
API_KEY = ''


class Listfiles:
    """

    La classe 'Listfiles' permets de vérifier et les extensions de fichiers présents
    et de converver leur noms dans un objet.
    """

    def __init__(self, path: str, ext: [str, list]):
        """

        :param path: chemin d'accès à vérifier.
        :param ext: extension de fichiers désirés.
        """
        self.path = path
        self.ext = ext
        self.files = []
        self.content = os.listdir(path)

        if not all(isinstance(s, str) for s in self.ext):
            raise Exception(f'Extension type Error: {self.ext} should be a str list')
        # Itération
        for f in self.content:
            file = f.split('.')
            try:
                name, extension = file[0], file[1]
            except IndexError:
                pass
            else:
                # Sauvegarde des fichiers
                if isinstance(self.ext, list):
                    if extension in self.ext:
                        self.files.append(name + '.' + extension)
                else:
                    if extension == self.ext:
                        self.files.append(name + '.' + extension)


class SearchApi:
    """

    Cette class permet d'utiliser l'API 'Programmable Search Engine' de Google.

    La méthode 'search' renvoie un dictionnaire des résultats trouvés sous la forme d'un titre: URL.
    La fonction '__add__' permet de conserver et mettre à jour les nouveau fichiers trouvés par la recherche.
    """

    def __init__(self, engine_id: str, api_key: str):
        """

        :param engine_id: id généré via 'programmablesearchengine''
        :param api_key: clé génréré via 'Custom Search JSON API''
        """
        self.engine_id = engine_id
        self.api_key = api_key
        self.subject = None
        self.start = 0
        self.query = None
        self.URL = f''
        self.ext = None
        self.results = {}

    def __add__(self, title: str, link: str):
        """

        :param title: titre contenu de la recherche
        :param link: URL du contenu de la recherche
        :return: void
        """
        self.results[title] = link
        if not os.stat('result.json').st_size == 0:
            with open('result.json', 'w') as docs:
                json.dump(self.results, docs)
                docs.close()
        else:
            with open('result.json', 'a') as docs:
                json.dump(self.results, docs)
                docs.close()

    def search(self, topic: str, filetype: [str, list], quantity: int):
        """

        :param topic: mot clé de la recherche
        :param filetype: extension du/des fichier(s) souhaité(s)
        :param quantity: nombre de résultats à rechercher
        :return: dictionnaire des résultats, titre: URL
        """

        if isinstance(filetype, list):
            filetype = '|'.join(i for i in filetype)
            print(filetype)
        self.query = f'filetype:{filetype} {topic}'
        self.URL = f"https://www.googleapis.com/customsearch/v1?key={self.api_key}&cx={self.engine_id}&q={self.query}&start={self.start}&num={quantity}"

        if not all(isinstance(s, str) for s in filetype):
            raise Exception(f'Extension type Error: {self.ext} should be a str list')

        # GET REQUEST API
        data = requests.get(self.URL).json()
        items = data.get('items')
        try:
            for i, content in enumerate(items, start=self.start):
                title = content.get("title")
                snippet = content.get("snippet")
                link = content.get("link")
                self.__add__(title, link)
            return self.results
        except TypeError:
            raise Exception(data['error']['message'])


def download(href: [str, list]):
    if not all(isinstance(s, str) for s in href):
        raise Exception(f'Href type Error: {href} should be a str list')

    # Comparaison contenu fichier / contenu du dossier
    # TODO: DL non téléchargés
    result_file = Listfiles(DEST_PATH, ext='json')
    if 'result.json' in result_file.files:
        try:
            with open('result.json', 'r') as source:
                s = json.load(source)
                source.close()
        finally:
            print(s)

    # Vérification ficher dump
    DIR = DEST_PATH + 'Documents'
    if not os.path.isdir(DIR):
        os.mkdir(DIR)
    else:
        pass

    # Téléchargement des fichiers
    counter = 0
    if isinstance(href, list):
        for href_ in href:
            doc_name = href_.split('/')[-1]
            data = urllib.request.urlretrieve(href_, DIR + f'/{doc_name}')
            counter += 1
    else:
        doc_name = href.split('/')[-1]
        urllib.request.urlretrieve(href, DIR + f'/{doc_name}')
        counter += 1
    print(f' [ {counter} ] fichiér(s) téléchargés dans {DIR}')


def main():
    web = SearchApi(ENGINE_ID, API_KEY)
    files = web.search('python', ['pdf', 'txt'], 12)
    href = [files[c] for i, c in enumerate(files)]
    download(href)


if __name__ == '__main__':
    main()
