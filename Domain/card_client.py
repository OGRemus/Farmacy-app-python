from Domain.entitate import Entitate


class CardClient(Entitate):
    def __init__(self, id_client, nume, prenume, CNP, data_nastere, data_inregistrare):
        super().__init__(id_client)
        self.__nume = nume
        self.__prenume = prenume
        self.__CNP = CNP
        self.__data_nastere = data_nastere
        self.__data_inregistrare = data_inregistrare

    @property
    def nume(self):
        return self.__nume

    @nume.setter
    def nume(self, val):
        self.__nume = val

    @property
    def prenume(self):
        return self.__prenume

    @prenume.setter
    def prenume(self, val):
        self.__prenume = val

    @property
    def CNP(self):
        return self.__CNP

    @CNP.setter
    def CNP(self, val):
        self.__CNP = val

    @property
    def data_nastere(self):
        return self.__data_nastere

    @data_nastere.setter
    def data_nastere(self, val):
        self.__data_nastere = val

    @property
    def data_inregistrare(self):
        return self.__data_inregistrare

    @data_inregistrare.setter
    def data_inregistrare(self, val):
        self.__data_inregistrare = val

    def __str__(self):
        return f"{self.id_entitate} - nume {self.nume}, prenume {self.prenume}, CNP {self.CNP}, "\
            f"data de nastere {self.data_nastere}, data_inregistrare {self.data_inregistrare}"

    def __repr__(self):
        return str(self)
