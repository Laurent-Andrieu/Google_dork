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

  Appelez le script avec les paramètres:
  ```bash
  Google_dork.py -t ANYTHING -e pdf -q 10 -c FR -k APIKEY -i ENGINEID
  ```
  Pour télécharger dans un dossier souhaité:
  ```bash
  Google_dork.py [paramètres] -f PATH
  ```
  Pour sélectionner uniquement les livres en ligne:
  ```bash
  Google_dork.py [paramètres] -b
  ```
  
  **Optionnellement**
  
  Modifiez le [sous fichier](https://github.com/Laurent-Andrieu/Google_dork/blob/master/Google_dork.py#L142) de téléchargement des fichiers:
  ```Python {.line-numbers}
  DIR = DEST_PATH + 'Documents'
  ```
