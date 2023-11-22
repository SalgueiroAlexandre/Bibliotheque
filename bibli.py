from simple_bibli import Simple_bibli
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import shutil
from Livre import Livre


class bibli(Simple_bibli):
    def __init__(self, path):
        self.livres = []
        super().__init__(path)

    def telecharger_livres(self, liens):
        for lien in liens:
            try:
                # Vérifie si le livre est déjà présent
                nom_fichier = os.path.basename(lien)
                if nom_fichier in self.livres:
                    print(f"Le livre {nom_fichier} est déjà présent.")
                    continue  # Passe au lien suivant

                # Envoie une requête GET pour récupérer le contenu du fichier
                response = requests.get(lien, stream=True, verify=False)

                # Vérifie si la requête a réussi (code 200 OK)
                if response.status_code == 200:
                    # Récupère le nom du fichier depuis l'URL
                    nom_fichier = os.path.basename(lien)

                    # Enregistre le fichier dans le dossier local
                    chemin_local = os.path.join(self.path, nom_fichier)
                    with open(chemin_local, 'wb') as fichier_local:
                        shutil.copyfileobj(response.raw, fichier_local)
                    self.livres.append(Livre(nom_fichier))
                    print(f"Le livre {nom_fichier} a été téléchargé et enregistré.")
                else:
                    print(f"Échec de la requête avec le code d'état : {response.status_code}")

            except Exception as e:
                print(f"Une erreur s'est produite lors du téléchargement du livre {lien} : {e}")

    def alimenter(self, url):
        try:
            # Envoie une requête GET à l'URL spécifiée
            response = requests.get(url, verify=False)
            # Vérifie si la requête a réussi (code 200 OK)
            if response.status_code == 200:
                # Analyse le contenu HTML de la page
                soup = BeautifulSoup(response.text, 'html.parser')

                # Récupère tous les liens avec un attribut href
                liens = soup.find_all('a', href=True)

                # Filtrer les liens se terminant par ".epub" ou ".pdf"
                liens_epub_pdf = [urljoin(url, lien['href']) for lien in liens if
                                  lien['href'].lower().endswith(('.epub', '.pdf'))]
                self.telecharger_livres(liens_epub_pdf)

                return liens_epub_pdf

            else:
                print(f"Échec de la requête avec le code d'état : {response.status_code}")
                return None

        except Exception as e:
            print(f"Une erreur s'est produite : {e}")
            return None


if __name__ == "__main__":
    bibli1 = bibli("./test")
    print(bibli1.path)
