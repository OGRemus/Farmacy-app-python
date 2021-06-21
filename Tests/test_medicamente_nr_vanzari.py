# {'augmentin': 4, 'paracetamol': 3, 'ibuprofen': 2}
from Domain.card_client_validator import CardClientValidator
from Domain.medicament_validator import MedicamentValidator
from Repo.file_repository import FileRepository
from Service.UndoRedoService import UndoRedoService
from Service.card_client_service import CardClientService
from Service.medicament_service import MedicamentService
from Service.tranzactie_service import TranzactieService
from Tests.common import clear_file


def test_medicamente_nr_vanzari():
    filename_meds = "test_meds_vanzari.txt"
    filename_cards = "test_cards_vanzari.txt"
    filename_tranz = "test_tranz_vanzari.txt"

    clear_file(filename_meds)
    clear_file(filename_cards)
    clear_file(filename_tranz)

    undoredo = UndoRedoService()

    card_client_repository = FileRepository(filename_cards)
    card_client_validator = CardClientValidator()
    service_card = CardClientService(card_client_repository, card_client_validator, undoredo)

    medicamente_repository = FileRepository(filename_meds)
    medicamente_validator = MedicamentValidator()
    undo = UndoRedoService()
    medicament_service = MedicamentService(medicamente_repository, medicamente_validator, undo)

    tranzactie_repository = FileRepository(filename_tranz)

    service_tranzactie = TranzactieService(medicamente_repository, card_client_repository, tranzactie_repository, undo)

    medicament_service.create("1", "paracetamol", "prod", 100, "NU")
    medicament_service.create("2", "augmentin", "prod", 300, "DA")
    medicament_service.create("3", "ibuprofen", "prod", 100, "NU")

    service_card.create("1", "ion", "pelea", "134", "1.nov.1980", "10.oct.2019")
    service_card.create("2", "petru", "rares", "123", "1.nov.1980", "10.oct.2019")
    service_card.create("3", "faiar", "sandu", "321", "1.nov.1980", "10.oct.2019")

    service_tranzactie.create("1", "1", "2", 10, "10.oct.2020,3.23.40")
    service_tranzactie.create("2", "1", "3", 2, "15.oct.2020,3.23.40")
    service_tranzactie.create("4", "1", "3", 2, "20.oct.2020,3.23.40")
    service_tranzactie.create("5", "2", "3", 2, "29.oct.2020,3.23.40")
    service_tranzactie.create("7", "2", "3", 2, "10.nov.2020,3.23.40")
    service_tranzactie.create("8", "2", "3", 2, "10.nov.2020,3.23.40")
    service_tranzactie.create("9", "2", "3", 2, "10.nov.2020,3.23.40")
    service_tranzactie.create("10", "3", "3", 2, "10.nov.2020,3.23.40")
    service_tranzactie.create("11", "3", "3", 2, "10.nov.2020,3.23.40")

    assert service_tranzactie.medicamente_nr_vanzari() == {'augmentin': 4, 'paracetamol': 3, 'ibuprofen': 2}


test_medicamente_nr_vanzari()

