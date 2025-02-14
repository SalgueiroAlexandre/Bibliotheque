from Bibliothèques.simple_bibli import Simple_bibli
from Livres.Livre_EPUB import Livre_EPUB
from Livres.Livre_PDF import Livre_PDF
import requests
import os
import shutil
import fonctions.fonctions_fichier as f

class bibli(Simple_bibli):
    def __init__(self, path="Default"):
        super().__init__(path)

    def telecharger(self, url):
            try:
                # Envoie une requête GET pour récupérer le contenu du fichier
                response = requests.get(url, stream=True, verify=False)

                # Vérifie si la requête a réussi (code 200 OK)
                if response.status_code == 200:
                    # Récupère le nom du fichier depuis l'URL
                    nom_fichier = os.path.basename(url)
                    # Enregistre le fichier dans le dossier local
                    chemin_local = os.path.join(self.path, nom_fichier)
                    with open(chemin_local, 'wb') as fichier_local:
                        shutil.copyfileobj(response.raw, fichier_local)
                    extension = os.path.splitext(nom_fichier)[1].lower()
                    match extension:
                        case '.epub':
                            livre = Livre_EPUB(os.path.join(self.path, nom_fichier))
                            self.livres.append(livre)
                            self.ajoute_auteur(livre)
                        case '.pdf':
                            livre = Livre_PDF(os.path.join(self.path, nom_fichier))
                            self.livres.append(livre)
                            self.ajoute_auteur(livre)
                        case _:
                            raise Exception("Extension pas prise en compte")
                    print(f"Le livre {nom_fichier} a été téléchargé et enregistré.")
                    return True
                else:
                    print(f"Échec de la requête avec le code d'état : {response.status_code}")
                    return False

            except Exception as e:
                print(f"Une erreur s'est produite lors du téléchargement du livre {url} : {e}")

    def alimenter(self, url, nbmax=10):
        try:
            liens_livres = f.recup_liens_livres(url)
            nblivres = 0  # compte le nombre de livres effectivement téléchargés
            for lien_livre in liens_livres:
                if self.telecharger(lien_livre):
                    nblivres += 1
                if nblivres >= nbmax:
                    break

        except requests.exceptions.RequestException as req_err:
            print(f"Erreur de requête : {req_err}")
            return None
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")
            return None
