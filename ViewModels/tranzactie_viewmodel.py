

class TranzactieViewModel:
    def __init__(self, id_tranzactie, medicament, card,numar_bucati, data_ora,pret, reducere ):
        self.id_tranzactie = id_tranzactie
        self.medicament = medicament
        self.card = card
        self.numar_bucati = numar_bucati
        self.data_ora = data_ora
        self.pret = pret
        self.reducere = reducere

    def __str__(self):
        return f"Tranzactia cu id-ul {self.id_tranzactie}, medicamentul {self.medicament},"\
            f"card {self.card}, numar_bucati {self.numar_bucati}, data si ora {self.data_ora}, pret {self.pret}, reducere {self.reducere}%"

