import json
import os
import urllib.request, urllib.error
import requests

# Directories
USER = os.getlogin()
PATH = f'C:/Users/{USER}/Downloads/'
DEST_PATH = f'C:/Users/{USER}/PycharmProjects/Google_dork/'
# API
ENGINE_ID = ''
API_KEY = ''


class Listfiles:
    """

    La classe 'Listfiles' permets de vérifier et les extensions de fichiers présents
    et de conserver leurs noms dans un objet.
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
    La fonction '__add__' permet de conserver et mettre à jour les nouveaux fichiers trouvés par la recherche.
    """

    def __init__(self, engine_id: str, api_key: str):
        """

        :param engine_id: id généré via 'programmablesearchengine''
        :param api_key: clé génréré via 'Custom Search JSON API''
        """
        self.engine_id = engine_id
        self.api_key = api_key
        self.subject = None
        self.query = None
        self.URL = f''
        self.ext = None
        self.results = {}
        self.json = {}

    def log(self, title: str, link: str):
        """

        :param title: Titre contenu de la recherche.
        :param link: URL du contenu de la recherche.
        :return: Void.
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

    def search(self, topic: str, filetype: [str, list], quantity: int, country: str, is_book=True):
        """

        :param topic: Mot clé de la recherche.
        :param filetype: Extension du/des fichier(s) souhaité(s).
        :param quantity: Nombre de résultats à rechercher.
        :param country: Zone géographique de la recherche.
        :param is_book: Recherche de livres uniquements.
        :return: Dictionnaire des résultats, titre: URL.
        """
        if not all(isinstance(s, str) for s in filetype):
            raise Exception(f'Extension type Error: {self.ext} should be a str list')

        # Extensions multiples
        if isinstance(filetype, list):
            filetype = '|'.join(i for i in filetype)

        # Précision de la recherche
        if not is_book:
            self.query = f'filetype:{filetype}%20{topic}'
        else:
            self.query = f'book:{topic}%20filetype:{filetype}'

        # Compteur de requêtes
        c = int((quantity + 9) / 10)
        for i in range(c):
            # Déterminer le start
            start = 1 + ((c - 1) * 10)
            # Déterminer le num
            num = int(((quantity / 10) % 1) * 10)
            if num == 0:
                num += 10
            self.URL = f"https://www.googleapis.com/customsearch/v1?key={self.api_key}" \
                       f"&cx={self.engine_id}&q={self.query}&start={start}&num={num}&cr=country{country}"

            # GET REQUEST API
            data = requests.get(self.URL).json()
            items = data.get('items')
            if items:
                for item, content in enumerate(items):
                    title = content.get("title")
                    link = content.get("link")
                    self.results[title] = link
                return self.results
            else:
                raise Exception(data['error']['message'])

    def download(self):
        # Vérification ficher dump
        DIR = DEST_PATH + 'Documents'
        if not os.path.isdir(DIR):
            os.mkdir(DIR)
        else:
            pass

        # Comparaison contenu fichier / contenu du dossier
        result_file = Listfiles(DEST_PATH, ext='json').files
        result_dir = Listfiles(DIR, ext='pdf').files
        if 'result.json' in result_file:
            try:
                with open('result.json', 'r') as source:
                    self.json = json.load(source)
                    source.close()
            except json.JSONDecodeError:
                pass

        # Téléchargement des fichiers
        counter = 0
        error = 0
        error_urls = []
        for title, href_ in self.results.items():
            doc_name = href_.split('/')[-1]
            try:
                if not href_ in self.json.values() or not doc_name in result_dir:
                    print(f'Téléchargement de: {doc_name}...\n\t{href_}')
                    urllib.request.urlretrieve(href_, DIR + f'/{doc_name}')
                    self.log(title, href_)
                    counter += 1
                else:
                    print(f'Précedement téléchargé: {doc_name}')
            except urllib.error.URLError:
                error += 1
                error_urls.append('\t'+href_)
        print(f'Taux d\'erreur: {error/counter}:') if counter else print(f'Erreur(s): {error}')
        print(*error_urls, sep='\n') if len(error_urls) != 0 else print()
        print(f'[ {counter} ] fichiér(s) téléchargés dans {DIR}')


def main():
    web = SearchApi(ENGINE_ID, API_KEY)
    web.search('python', 'pdf', 10, 'FR')
    web.download()


if __name__ == '__main__':
    main()
