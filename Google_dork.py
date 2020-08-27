import json
import optparse
import os
import urllib.error
import urllib.request
import requests

PATH = os.getcwd()
# Ajustement chemin d'accès
if os.name == 'nt':
    PATH = PATH.replace('\\', '/')


def arg():
    """

    La fonction arg retourne les arguments lors de l'appel du script.
    """
    parser = optparse.OptionParser(usage='utilisation: %prog [options] [-t] [-e] [-c] [-a] [-i]', version='%prog v1.0')

    # Main parameters
    parser.add_option('-t', '--topic', dest='topic', help='Sujet à rechercher', type=str)
    parser.add_option('-e', '--extension', dest='ext', help='Nom des extensions souhaités', type=str)
    parser.add_option('-q', '--quantity', dest='quantity', help='Quantité de fichiers', type=int)
    parser.add_option('-c', '--country', dest='country', help='Country Code XX', type=str)

    # Options
    group = optparse.OptionGroup(parser, 'More options')
    group.add_option('-b', '--books', dest='book', help='Rechercher des livres uniquements', action='store_true',
                     default=False)
    group.add_option('-f', '--folder', dest='folder', type="str",
                     help="Chemin d'accès du dossier où stocker les fichiers téléchargés", default=PATH)
    parser.add_option_group(group)

    # API credentials parameters
    group = optparse.OptionGroup(parser, 'Api creditentials')
    group.add_option('-k', '--api_key', dest='key', help="Clé de l'API Google CSE", type=str)
    group.add_option('-i', '--id', dest='id', help="ID de l'API Google CSE", type=str)
    parser.add_option_group(group)

    (options, args) = parser.parse_args()

    # Options nécessaires
    missing = []
    for k, v in vars(options).items():
        if k != 'book' or 'folder':
            if v is None:
                missing.append(k)
    if len(missing) != 0:
        parser.error(f'Missing values for {missing}')
    else:
        return options


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
    La fonction 'log' permet de conserver et mettre à jour les nouveaux fichiers trouvés par la recherche.
    La méthode 'download' permet de télécharger les fichiers trouvés non déjà téléchargés.
    """

    def __init__(self, engine_id: str, api_key: str, path: str):
        """

        :param engine_id: ID généré via 'programmablesearchengine''
        :param api_key: Clé génréré via 'Custom Search JSON API''
        :param path: Chemin d'accès
        """
        self.engine_id = engine_id
        self.api_key = api_key
        self.query = None
        self.URL = f''
        self.ext = None
        self.results = {}
        self.json = {}
        self.path = path
        if os.name == 'nt':
            self.path = self.path.replace('\\', '/')
        if not os.path.isdir(self.path):
            os.mkdir(self.path)

    def log(self, title: str, link: str):
        """

        :param title: Titre contenu de la recherche.
        :param link: URL du contenu de la recherche.
        :return: Void.
        """
        self.results[title] = link

        # Vérification ficher log
        if 'log.json' not in os.listdir(self.path):
            open(f'{self.path}/log.json', 'a+').close()
        else:
            pass

        if not os.stat(f'{self.path}/log.json').st_size == 0:
            with open(f'{self.path}/log.json', 'w') as docs:
                json.dump(self.results, docs)
                docs.close()
        else:
            with open(f'{self.path}/log.json', 'a') as docs:
                json.dump(self.results, docs)
                docs.close()

    def search(self, topic: str, filetype: [str, list], quantity: int, country: str, is_book=False):
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
        DIR = self.path + '/Documents/'
        # Vérification dossier dump
        if not os.path.isdir(DIR):
            os.mkdir(DIR)
        else:
            pass

        # Comparaison contenu fichier / contenu du dossier
        result_file = Listfiles(PATH, ext='json').files
        result_doc = Listfiles(DIR, ext='pdf').files
        if 'log.json' in result_file:
            try:
                with open('log.json', 'r') as source:
                    self.json = json.load(source)
                    source.close()
            except json.JSONDecodeError:
                pass

        # Téléchargement des fichiers
        counter = 0
        error = 0
        error_urls = []
        # Url correction
        remove_list = "?><\/:\"*|"
        for title, href_ in self.results.items():
            doc_name = href_.split('/')[-1]
            for char in remove_list:
                if char in doc_name:
                    doc_name = doc_name.replace(char, "")
            try:
                if href_ not in self.json.values() and doc_name not in result_doc:
                    print(f'Téléchargement de: {doc_name}...\n\t{href_}')
                    urllib.request.urlretrieve(href_, DIR + doc_name)
                    self.log(title, href_)
                    counter += 1
                else:
                    print(f'Précedement téléchargé: {doc_name}')
            except urllib.error.URLError:
                error += 1
                error_urls.append('\t' + href_)
        print(f'Erreur(s): {error}')
        print(*error_urls, sep='\n') if len(error_urls) != 0 else print()
        print(f'[ {counter} ] fichiér(s) téléchargés dans {DIR}')

        # Vérification extension des fichiers
        dl_files = os.listdir(DIR)
        for k, fs in enumerate(dl_files):
            try:
                fs.split('.')
            except ValueError:
                os.replace(DIR+fs, DIR+fs+'.pdf')


def main():
    args = arg()
    web = SearchApi(args.id, args.key, args.folder)
    web.search(args.topic, args.ext, args.quantity, args.country, args.book)
    web.download()


if __name__ == '__main__':
    main()
