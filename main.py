from Domain.card_client_validator import CardClientValidator
from Domain.medicament_validator import MedicamentValidator
from Repo.file_repository import FileRepository
from Service.UndoRedoService import UndoRedoService
from Service.card_client_service import CardClientService
from Service.medicament_service import MedicamentService
from Service.tranzactie_service import TranzactieService
from Tests.run_all import run_all
from UI.console import Console

def add_data():
    medicament_repository = FileRepository("medicamente.txt")
    card_client_repository = FileRepository("carduri.txt")
    tranzactii_repository = FileRepository("tranzactii.txt")

    medicament_validator = MedicamentValidator()
    card_validator = CardClientValidator()

    medicament_service = MedicamentService(medicament_repository, medicament_validator)
    card_client_service = CardClientService(card_client_repository, card_validator)
    tranzactii_service = TranzactieService(medicament_repository, card_client_repository, tranzactii_repository)

    medicament_service.create("1", "paracetamol", "prod", 100, "NU")
    medicament_service.create("2", "augmentin", "prod", 300, "DA")
    medicament_service.create("3", "ibuprofen", "prod", 100, "NU")

    card_client_service.create("1", "ion", "pelea", "134", "1.nov.1980", "10.oct.2019")
    card_client_service.create("2", "petru", "rares", "123", "1.nov.1980", "10.oct.2019")
    card_client_service.create("3", "faiar", "sandu", "321", "1.nov.1980", "10.oct.2019")

    tranzactii_service.create("1", "1", "2", 10, "10.oct.2020, 3.23.40")
    tranzactii_service.create("2", "1", "3", 2, "15.oct.2020, 3.23.40")
    tranzactii_service.create("4", "1", "3", 2, "20.oct.2020, 3.23.40")
    tranzactii_service.create("5", "2", "3", 2, "29.oct.2020, 3.23.40")
    tranzactii_service.create("7", "2", "3", 2, "10.nov.2020, 3.23.40")
    tranzactii_service.create("8", "2", "3", 2, "10.nov.2020, 3.23.40")
    tranzactii_service.create("9", "2", "3", 2, "10.nov.2020, 3.23.40")
    tranzactii_service.create("10", "3", "3", 2, "10.nov.2020, 3.23.40")
    tranzactii_service.create("11", "3", "3", 2, "10.nov.2020, 3.23.40")


def main():
    run_all()
    medicament_repository = FileRepository("medicamente.txt")
    card_client_repository = FileRepository("carduri.txt")
    tranzactii_repository = FileRepository("tranzactii.txt")

    medicament_validator = MedicamentValidator()
    card_validator = CardClientValidator()
    # add_data()
    undoredo = UndoRedoService()
    medicament_service = MedicamentService(medicament_repository, medicament_validator, undoredo)

    card_client_service = CardClientService(card_client_repository, card_validator,undoredo)

    tranzactii_service = TranzactieService(medicament_repository, card_client_repository, tranzactii_repository, undoredo)

    medicament_service.export_csv()



    #"%d.%b.%Y,%H.%M.%S"

    user_interface = Console(medicament_service, card_client_service, tranzactii_service,undoredo)
    user_interface.run_console()




main()
