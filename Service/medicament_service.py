import string
from copy import deepcopy
import random

from Domain.medicament import Medicament
from Domain.medicament_validator import MedicamentValidator
from Domain.undo_add import UndoAdd
from Domain.undo_delete import UndoDelete
from Domain.undo_update import UndoUpdate
from Exceptions.medicament_exception import InvalidMedicamentException
from Repo.ExportExcel import ExportExcel
from Repo.file_repository import FileRepository
from Service.UndoRedoService import UndoRedoService


class MedicamentService:
    def __init__(self, medicament_repository: FileRepository, medicament_validator: MedicamentValidator
                 , undo_redo_service: UndoRedoService):
        self.__medicament_repository = medicament_repository
        self.__medicament_validator = medicament_validator
        self.__undo_redo_service = undo_redo_service

    def create(self, id_medicament, nume, producator, pret, reteta):
        medicament = Medicament(id_medicament, nume, producator, pret, reteta)
        if reteta == "DA":
            medicament.reteta = True
        elif reteta == "NU":
            medicament.reteta = False
        self.__medicament_validator.validate(medicament)
        self.__medicament_repository.create(medicament)
        self.__undo_redo_service.add_to_undo(UndoAdd(medicament, self.__medicament_repository))
        self.export_csv()

    def delete(self, id_medicament):
        for medicament in self.__medicament_repository.get_all():
            if id_medicament == medicament.id_entitate:
                self.__medicament_repository.delete(id_medicament)
                self.__undo_redo_service.add_to_undo(UndoDelete(medicament, self.__medicament_repository))
                self.export_csv()
                return

        raise InvalidMedicamentException("Medicamentul nu exista")

    def update(self, id_medicament, nume, producator, pret, reteta):

        medicament_vechi = self.__medicament_repository.find_by_id(id_medicament)
        medicament = Medicament(id_medicament, nume, producator, pret, reteta)

        if medicament_vechi is None:
            raise KeyError(f"Medicamentul cu id-ul {id_medicament} nu exista!")
        if nume != "":
            medicament.nume = nume

        if producator != "":
            medicament.producator = producator

        if pret != "":
            medicament.pret = pret

        if reteta != "":
            medicament.reteta = reteta

        if reteta == "DA" or reteta == "":
            medicament.reteta = True
        else:
            medicament.reteta = False

        self.__medicament_repository.update(medicament)
        self.__undo_redo_service.add_to_undo(UndoUpdate(medicament_vechi, medicament, self.__medicament_repository))
        self.export_csv()

    def get_all(self):
        return self.__medicament_repository.get_all()

    def operatie_scumpire(self, medicament, procent):
        medicament.pret = medicament.pret + medicament.pret*(procent/100)
        return medicament

    def scumpire(self, valoare, procent):
        """
        Scumpeste medicamentele cu pretul mai mic decat valoare cu procentul procent
        :param valoare: o valoare data
        :param procent: un procent
        :return:
        """
        # for medicament in self.__medicament_repository.get_all():
        #     if medicament.pret < valoare:
        #         medicament.pret = medicament.pret + medicament.pret * (procent/100)
        #         self.__medicament_repository.update(medicament)
        lista_medicamente_scumpite = map(lambda x: self.operatie_scumpire(x, procent), filter(lambda x: x.pret < valoare, self.__medicament_repository.get_all()))
        for medicament in lista_medicamente_scumpite:
            self.__medicament_repository.update(medicament)
        self.export_csv()

    def populate_entities(self, n):
        """
        Populeaza entitatile cu valori random valide
        :param n:
        :return:
        """
        lettters = string.ascii_lowercase

        id = random.randint(10, 150)
        nume = "".join(random.choice(lettters) for i in range(10))
        producator = "".join(random.choice(lettters) for i in range(10))
        pret = random.randint(1, 10000)
        reteta = random.choice([True, False])
        medicament = Medicament(id, nume, producator, pret, reteta)
        self.__medicament_repository.create(medicament)
        if n == 0:
            self.export_csv()
        else:
            self.populate_entities(n-1)

    def cautare(self, tip, var):
        """
        cauta in fisier medicamentele dupa var 
        :param tip: tipul cheii dupa care cauta
        :param var: variabila cautata
        :return: rezultatele cautarii
        """
        rezultat_cautare = []
        for medicament in self.__medicament_repository.get_all():
            if tip == "nume":
                if var == medicament.nume:
                    rezultat_cautare.append(medicament)
            elif tip == "producator":
                if var == medicament.producator:
                    rezultat_cautare.append(medicament)
            elif tip == "pret":
                if int(var) == medicament.pret:
                    rezultat_cautare.append(medicament)
            elif tip == "reteta":
                if bool(var) == medicament.reteta:
                    rezultat_cautare.append(medicament)
            elif tip == "text":
                fields = []
                for fieldValue in vars(medicament).values():
                    fields.append(str(fieldValue))
                for field in fields:
                    if var in field:
                        rezultat_cautare.append(medicament)
            else:
                print("Introduceti un tip de cautare valid")
        return rezultat_cautare

    def export_csv(self):
        """
        Functie de export in fisierul csv al medicamente repo
        :return: none
        """
        ExportExcel.write(self.__medicament_repository.get_all())
