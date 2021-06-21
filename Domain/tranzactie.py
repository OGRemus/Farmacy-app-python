from Domain.entitate import Entitate
from datetime import datetime


class Tranzactie(Entitate):
    def __init__(self, id_tranzactie, id_medicament, id_card_client, nr_bucati, data_ora, pret, reducere):
        super().__init__(id_tranzactie)
        self.id_medicament = id_medicament
        self.id_card_client = id_card_client
        self.nr_bucati = nr_bucati
        self.data_ora = data_ora
        self.pret = pret
        self.reducere = reducere

    def __str__(self):
        return f"{self.id_entitate} -id medicament {self.id_medicament}, id card client{self.id_card_client}"\
            f"numar bucati {self.nr_bucati}, data_ora{self.data_ora}, pret {self.pret}, reducere {self.reducere}"



