# Google_dork

Script python permettant l'utilisation de la syntaxe des 'Google dorks' via l'API google afin de télécharger des fichiers à partir d'un sujet.

---

## Cloner le repository

### Windows
* Télécharger & Installer [Git Bash](https://gitforwindows.org/).

### Linux 
* Entrer `sudo apt install git` dans le terminal.

Enfin entrez `git clone https://github.com/Laurent-Andrieu/Spotify-Lyrics/` pour cloner le repository.

---

## Requirements

### Python packages
* [Python Version 3.8](https://www.python.org/downloads/release/python-382/)
* json
* os
* urllib
* [requests](https://pypi.org/project/requests/)

### API creditentials
Créer un CSE:
  * [CustomSearchEngine](https://programmablesearchengine.google.com/cse/all)
  
Générer une clé API limitée:
  * [Custom Search JSON API](https://developers.google.com/custom-search/v1/introduction)
---

## API info+
[Using REST](https://developers.google.com/custom-search/v1/using_rest)

## Utilisation

### <u>Variables:</u>

Modifiez les [chemins d'accès](https://github.com/Laurent-Andrieu/Google_dork/blob/master/Google_dork.py#L9) nécessaire:
  ```Python
  PATH = f'C:/Users/{USER}/Downloads/' # emplacement du fichier des téléchargements.
  
  DEST_PATH = f'C:/Users/{USER}/PycharmProjects/' # emplacement souhaité pour la copie des fichiers (un sous dossier 'Documents' y sera créé).
  ```

Modifiez les [identifiants de l'API](https://github.com/Laurent-Andrieu/Google_dork/blob/master/Google_dork.py#L12):
  ```Python
  ENGINE_ID = '' # aussi appelé cx, identifie l'api.
  API_KEY = '' # clée de l'api.
  ```
  
  Modifiez le(s) mot(s) clé(s) à rechercher ansi que les type d'extensions de fichiers désirés:
  ```Python
  def main():
    web = SearchApi(ENGINE_ID, API_KEY)
    web.search('python', 'pdf', 10, 'FR')
    web.download()
  ```
  
  **Optionnellement**
  
  Modifiez le [sous fichier](https://github.com/Laurent-Andrieu/Google_dork/blob/master/Google_dork.py#L142) de téléchargement des fichiers:
  ```Python {.line-numbers}
  DIR = DEST_PATH + 'Documents'
  ```
