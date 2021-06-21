from Domain.medicament import Medicament
from Domain.medicament_validator import MedicamentValidator
from Repo.file_repository import FileRepository
from Service.UndoRedoService import UndoRedoService
from Service.medicament_service import MedicamentService
from Tests.common import clear_file


def test_scumpire():
    filename = "test_scumpire.txt"
    clear_file(filename)
    medicament_repository = FileRepository(filename)
    medicament_validator = MedicamentValidator()
    undoredo = UndoRedoService()
    service = MedicamentService(medicament_repository, medicament_validator, undoredo)
    service.create("100", "paracetamol", "prod", 100, "NU")

    service.scumpire(200, 50)

    for med in service.get_all():
        if med.id_entitate == "100":
            assert med.pret == 150

