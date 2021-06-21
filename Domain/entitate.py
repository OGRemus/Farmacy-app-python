class Entitate:

    def __init__(self, id_entitate):
        self.__id_entitate = id_entitate

    @property
    def id_entitate(self):
        return self.__id_entitate

    def __eq__(self, other):
        return type(self) == type(other) and self.__id_entitate == other.__id_entitate

