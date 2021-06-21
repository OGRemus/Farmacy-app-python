from Domain.medicament import Medicament
from Service.UndoRedoService import UndoRedoService
from Service.card_client_service import CardClientService
from Service.medicament_service import MedicamentService
from Service.tranzactie_service import TranzactieService


def test_service():


    medicament_service = MedicamentService
    card_service = CardClientService
    trans_service = TranzactieService


    undoredo = UndoRedoService()
    med = Medicament("test","test", "test",1,"DA")
    medicament_service.create(med,undoredo)


