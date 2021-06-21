import operator
from copy import deepcopy
from datetime import datetime


from Domain.medicament import Medicament
from Domain.tranzactie import Tranzactie
from Domain.undo_add import UndoAdd
from Domain.undo_delete import UndoDelete
from Domain.undo_update import UndoUpdate
from Exceptions.invalid_card_exception import InvalidCardException
from Repo.file_repository import FileRepository
from Service.UndoRedoService import UndoRedoService
from ViewModels.tranzactie_viewmodel import TranzactieViewModel


class TranzactieService:
    def __init__(self,
                 medicamente_repository: FileRepository,
                 card_client_repository: FileRepository,
                 tranzactie_repository: FileRepository,
                 undoredo_service : UndoRedoService):
        self.__medicamente_repository = medicamente_repository
        self.__card_client_repository = card_client_repository
        self.__tranzactie_repository = tranzactie_repository
        self.__undoredo_service = undoredo_service

    def create(self, id_tranzactie, id_medicament, id_card_client, nr_bucati, data_ora):
        """
        creeaza o tranzactie noua
        :param id_tranzactie: string
        :param id_medicament: string
        :param id_card_client: string
        :param nr_bucati: int
        :param data_ora: datetime
        :return: none
        """

        medicament = self.__medicamente_repository.find_by_id(id_medicament)
        if medicament is None:
            raise KeyError(f"Nu exista nici un medicament cu id-ul {id_medicament}")

        pret = (nr_bucati) * medicament.pret

        if self.__card_client_repository.find_by_id(id_card_client) is not None:
            if medicament.reteta is False:
                reducere = 10
            else:
                reducere = 15
        else:
            reducere = 0

        pret = pret - (pret * (reducere / 100))

        tranzactie = Tranzactie(id_tranzactie, id_medicament, id_card_client, nr_bucati, data_ora, pret, reducere)
        self.__undoredo_service.add_to_undo(UndoAdd(tranzactie,self.__tranzactie_repository))
        self.__tranzactie_repository.create(tranzactie)

    def get_all(self):
        viewmodels = []
        for tranzactie in self.__tranzactie_repository.get_all():
            medicament = self.__medicamente_repository.find_by_id(tranzactie.id_medicament)
            card = self.__card_client_repository.find_by_id(tranzactie.id_card_client)
            viewmodels.append(TranzactieViewModel(tranzactie.id_entitate, medicament, card, tranzactie.nr_bucati, tranzactie.data_ora, tranzactie.pret, tranzactie.reducere))

        return viewmodels

    def delete(self, id_tranzactie):
        tranzactie = self.__tranzactie_repository.find_by_id(id_tranzactie)
        self.__undoredo_service.add_to_undo(UndoDelete(tranzactie, self.__tranzactie_repository))
        self.__tranzactie_repository.delete(id_tranzactie)

    def update(self, id_tranzactie, id_medicament, id_card_client, nr_bucati, data_ora):
        tranzactie_veche = self.__tranzactie_repository.find_by_id(id_tranzactie)
        if self.__tranzactie_repository.find_by_id(id_tranzactie) is None:
            raise KeyError(f"Tranzactia cu id-ul {id_tranzactie} nu exista !")
        if self.__medicamente_repository.find_by_id(id_medicament) is None:
            raise KeyError(f"Nu exista medicamentul cu id-ul {id_medicament}")
        if self.__card_client_repository.find_by_id(id_card_client) is None:
            id_card_client = ''
        if nr_bucati <= 0:
            raise ValueError(f"Numarul de bucati {nr_bucati} trebuie sa fie pozitiv")
        medicament = self.__medicamente_repository.find_by_id(id_medicament)
        if self.__card_client_repository.find_by_id(id_card_client) is not None:
            if medicament.reteta is False:
                reducere = 10
            else:
                reducere = 15
        else:
            reducere = 0
        pret = self.__medicamente_repository.find_by_id(id_medicament).pret * nr_bucati
        pret = pret - (pret * (reducere / 100))

        # if pret != nr_bucati * medicament.pret:
        #     raise ValueError("Nu puteti schimba pretul tranzactiei fara a schimba cantitatea de medicamente sau pretul")
        tranzactie = Tranzactie(id_tranzactie, id_medicament, id_card_client, nr_bucati, data_ora, pret, reducere)
        self.__undoredo_service.add_to_undo(UndoUpdate(tranzactie_veche,tranzactie,self.__tranzactie_repository))
        self.__tranzactie_repository.update(tranzactie)

    def tranzactii_pe_interval(self, data1, data2):
        """
        LAMBDA SI FILTER
        Afiseaza tranzactiile dintr un anumit interval de timp
        :param data1: data de start
        :param data2: data de finish
        :return:
        """
        if data1 > data2:
            raise ValueError("Prima data e dupa a doua data")

        # for tranzactie in self.__tranzactie_repository.get_all():
        #     if data1 < tranzactie.data_ora.date() < data2:
        #         print(tranzactie)

        tranzactii_filtrate = filter(lambda x : data1 < x.data_ora.date() < data2 ,self.__tranzactie_repository.get_all())
            # if data1 < datetime.strptime(tranzactie.data_ora, "%d.%b.%Y, %H.%M.%S").date() < data2:
            #     print(tranzactie)
        return tranzactii_filtrate

    def stergere_tranzactii_pe_interval(self, data1, data2):
        """
        sterge tranzactiile dintr-un anumit interval
        :param data1: data de start
        :param data2: data de finish
        :return:
        """
        if data1 > data2:
            raise ValueError("Prima data e dupa a doua data")

        for tranzactie in self.__tranzactie_repository.get_all():

            if data1 < tranzactie.data_ora.date() < data2:
                self.__tranzactie_repository.delete(tranzactie.id_entitate)

    def medicamente_nr_vanzari(self):
        """
        Returneaza un dictionar medicamentele sortate descrescator dupa numarul de tranzactii
        :return: dictionar
        """
        vanzari = {}
        for tranzactie in self.__tranzactie_repository.get_all():
            if self.__medicamente_repository.find_by_id(tranzactie.id_medicament).nume not in vanzari:
                vanzari[self.__medicamente_repository.find_by_id(tranzactie.id_medicament).nume] = 1
            else:
                vanzari[self.__medicamente_repository.find_by_id(tranzactie.id_medicament).nume] += 1
        # vanzari_tuples = reversed(sorted(vanzari.items(), key=operator.itemgetter(1)))
        vanzari_tuples = self.mergeSort(list(vanzari.items()), key = operator.itemgetter(1), reverse=True)
        sorted_vanzari = {k: v for k, v in vanzari_tuples}

        return sorted_vanzari

    def ordoneaza_card_client_dupa_reduceri(self):
        """
        Returneaza un dictionar cu cardurile ordonate descrescator dupa valoarea reducerilor obtinute
        :return: dictionar
        """
        carduri = {}
        for tranzactie in self.__tranzactie_repository.get_all():
            medicament = self.__medicamente_repository.find_by_id(tranzactie.id_medicament)
            if self.__card_client_repository.find_by_id(tranzactie.id_card_client).id_entitate in carduri:
                carduri[self.__card_client_repository.find_by_id(tranzactie.id_card_client).id_entitate] = carduri[self.__card_client_repository.find_by_id(tranzactie.id_card_client).id_entitate] + ( (medicament.pret * tranzactie.nr_bucati)- tranzactie.pret)
            else:
                carduri[self.__card_client_repository.find_by_id(tranzactie.id_card_client).id_entitate] =  (medicament.pret * tranzactie.nr_bucati) - tranzactie.pret

        carduri_touples = reversed(sorted(carduri.items(), key=operator.itemgetter(1)))
        sorted_carduri = {k: v for k, v in carduri_touples}
        return sorted_carduri

    def mergeSort(self, lst, key=lambda x: x, reverse=False):
        """
        sorteaza o lista folosind algoritmul merge Sort si returneaza lista sortata
        :param key: cheia dupa care se face sortarea
        :param cmp:criteriul de comparatie
        :param reverse: specifica daca sortarea se face invers sau nu
        :return: lista rezultata
        """
        myList = deepcopy(lst)

        def helper(arr):
            if len(arr) > 1:
                mid = len(arr) // 2  # Finding the mid of the array
                L = arr[:mid]  # Dividing the array elements
                R = arr[mid:]  # into 2 halves

                helper(L)  # Sorting the first half
                helper(R)  # Sorting the second half

                i = j = k = 0

                # Copy data to temp arrays L[] and R[]
                while i < len(L) and j < len(R):
                    if key(L[i]) < key(R[j]):
                        arr[k] = L[i]
                        i += 1
                    else:
                        arr[k] = R[j]
                        j += 1
                    k += 1

                # Checking if any element was left
                while i < len(L):
                    arr[k] = L[i]
                    i += 1
                    k += 1

                while j < len(R):
                    arr[k] = R[j]
                    j += 1
                    k += 1

            else:
                return arr

        helper(myList)

        if reverse:
            myList = list(reversed(myList))

        return myList


    def ordoneaza_card_client_dupa_reduceri_2(self):
        carduri = []
        for tranzactie in self.__tranzactie_repository.get_all():
            medicament = self.__medicamente_repository.find_by_id(tranzactie.id_medicament)
            carduri.append([tranzactie.id_card_client, (medicament.pret * tranzactie.nr_bucati) - tranzactie.pret])

    def delete_all_tranzactii_medicament(self, id_medicament):
        """
        sterge toate tranzactiile cu care au medicamentul id medicament
        :param id_medicament:
        :return:
        """
        for tranz in self.__tranzactie_repository.get_all():
            if tranz.id_medicament == id_medicament:
                self.__tranzactie_repository.delete(tranz.id_entitate)

