from base_livre import *

class Livre(base_livre):
    def __init__(self,ressource):
        self.arg = [] #dictionnaire
        #self.arg[]=recup_pdf(ressource)

    def titre(self):
        return self.arg["titre"]

    def auteur(self):
        return self.arg["auteur"]

    def langue(self):
        return self.arg["langue"]

    def sujet(self):
        return self.arg["sujet"]

    def date(self):
        return self.arg["date"]