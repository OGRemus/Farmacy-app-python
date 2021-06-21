from Domain.entitate import Entitate


class Medicament(Entitate):
    def __init__(self, id_medicament, nume, producator, pret, reteta):
        super().__init__(id_medicament)
        self.__nume = nume
        self.__producator = producator
        self.__pret = pret
        self.__reteta = reteta

    @property
    def nume(self):
        return self.__nume

    @nume.setter
    def nume(self, val):
        self.__nume = val

    @property
    def producator(self):
        return self.__producator

    @producator.setter
    def producator(self, val):
        self.__producator = val

    @property
    def pret(self):
        return self.__pret

    @pret.setter
    def pret(self, val):
        self.__pret = val

    @property
    def reteta(self):
        return self.__reteta

    @reteta.setter
    def reteta(self, val):
        self.__reteta = val

    def __str__(self):
        return f"{self.id_entitate} - nume: {self.__nume}, producator: {self.producator}, pret: {self.pret}, "\
            f"necesita reteta: {self.reteta}"

    def __repr__(self):
        return str(self)

