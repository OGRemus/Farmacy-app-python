from Domain.medicament_validator import MedicamentValidator
from Repo.file_repository import FileRepository
from Service.UndoRedoService import UndoRedoService
from Service.medicament_service import MedicamentService
from Tests.common import clear_file


def test_create_medicament():
    filename = "medicament_test.txt"
    clear_file(filename)
    medicament_repository = FileRepository(filename)
    medicament_validator = MedicamentValidator()
    undoredo = UndoRedoService()

    service = MedicamentService(medicament_repository, medicament_validator, undoredo)
    service.create("1", "paracetamol", "prod", 100, "NU")
    assert len(service.get_all()) == 1
    try:
        service.create("1", "paracetamol", "prod", 100, "NU")
        assert False
    except KeyError:
        assert True
    except Exception as ex:
        assert False
    assert len(service.get_all()) == 1

    try:
        service.create("2", "augmentin", "prod", -300, "DA")
        assert False
    except ValueError:
        assert True
    except Exception:
        assert False
    assert len(service.get_all()) == 1

    added = medicament_repository.find_by_id("1")
    assert added is not None
    assert added.id_entitate == "1"
    assert added.nume == "paracetamol"
    assert added.producator == "prod"
    assert added.pret == 100
    assert added.reteta is False

