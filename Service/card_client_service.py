from datetime import datetime, date

from Domain.card_client import CardClient
from Domain.card_client_validator import CardClientValidator
from Domain.undo_add import UndoAdd
from Domain.undo_delete import UndoDelete
from Domain.undo_update import UndoUpdate
from Repo.file_repository import FileRepository
from Service.UndoRedoService import UndoRedoService


class CardClientService:
    def __init__(self, card_client_repository: FileRepository, card_client_validator: CardClientValidator,
                 undo_redo_service : UndoRedoService):
        self.__card_client_repository = card_client_repository
        self.__card_client_validator = card_client_validator
        self.__undo_redo_service = undo_redo_service

    def create(self, id_card_client, nume, prenume, CNP, data_nastere, data_inregistrare):
        card_client = CardClient(id_card_client, nume, prenume, CNP, data_nastere, data_inregistrare)
        self.__card_client_validator.validate(card_client)
        data_inregistrare = datetime.strptime(data_inregistrare, "%d.%b.%Y").date()
        data_nastere = datetime.strptime(data_nastere, "%d.%b.%Y").date()
        card_client = CardClient(id_card_client, nume, prenume, CNP, data_nastere, data_inregistrare)
        self.__undo_redo_service.add_to_undo(UndoAdd(card_client, self.__card_client_repository))
        self.__card_client_repository.create(card_client)

        return self.__card_client_repository.get_all()

    def get_all(self):
        return self.__card_client_repository.get_all()

    def delete(self, id_card):
        for card_client in self.__card_client_repository.get_all():
            if id_card == card_client.id_entitate:
                self.__card_client_repository.delete(id_card)
                self.__undo_redo_service.add_to_undo(UndoDelete(card_client,self.__card_client_repository))
                return
        raise ValueError("Id-ul nu exista")

    def update(self, id_card, nume, prenume, cnp, data_nastere, data_inregistrare):
        card = self.__card_client_repository.find_by_id(id_card)
        card_nou = CardClient(id_card, nume, prenume, cnp, data_nastere, data_inregistrare)

        if card is None:
            raise KeyError(f"Cardul cu id-ul {id_card} nu exista!")

        if nume != "":
            card.nume = nume
        if prenume != "":
            card.prenume = prenume
        if cnp != "":
            card.CNP = cnp
        if data_nastere != "":
            card.data_nastere = datetime.strptime(data_nastere, "%d.%b.%Y")
        if data_inregistrare != "":
            card.data_inregistrare = datetime.strptime(data_inregistrare, "%d.%b.%Y")

        self.__undo_redo_service.add_to_undo(UndoUpdate(card,card_nou,self.__card_client_repository))

        self.__card_client_repository.update(card)

    def cautare(self, tip, var):
        """
        Functie de cautare carduri client in fisier
        :param tip: tipul cautarii
        :param var: variabila cautata
        :return: lista de rezultate
        """
        rezultat_cautare = []
        for card in self.__card_client_repository.get_all():
            if tip == "nume":
                if var in card.nume:
                    rezultat_cautare.append(card)
            elif tip == "prenume":
                if var in card.prenume:
                    rezultat_cautare.append(card)
            elif tip == "cnp":
                if var in str(card.CNP):
                    rezultat_cautare.append(card)
            elif tip == "data nastere":
                if var in str(card.data_nastere):
                    rezultat_cautare.append(card)
            elif tip == "data inregistrare":
                if var in str(card.data_inregistrare):
                    rezultat_cautare.append(card)
            elif tip == "text":
                fields = []
                for fieldValue in vars(card).values():
                    fields.append(str(fieldValue))
                for field in fields:
                    if var in field:
                        rezultat_cautare.append(card)
        return rezultat_cautare







