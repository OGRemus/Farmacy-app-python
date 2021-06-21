from Domain.medicament import Medicament
from Repo.file_repository import FileRepository
from Tests.common import clear_file


def test_file_repository():
    filename = "medicamente_test.txt"
    clear_file(filename)
    medicament_repository = FileRepository(filename)

    assert medicament_repository.get_all() == []

    m = Medicament("1", "paracetamol", "prod", 100, "NU")
    medicament_repository.create(m)

    assert medicament_repository.get_all() == [m]

