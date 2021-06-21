from Tests.test_domain import test_domain
from Tests.test_file_repository import test_file_repository
from Tests.test_medicament_service import test_create_medicament
from Tests.test_medicamente_nr_vanzari import test_medicamente_nr_vanzari
from Tests.test_ordoneaza_card_reduceri import test_ordoneaza_card_dupa_reduceri
from Tests.test_scumpire import test_scumpire


def run_all():
    test_domain()
    test_file_repository()
    test_create_medicament()
    test_ordoneaza_card_dupa_reduceri()
    test_medicamente_nr_vanzari()
    test_scumpire()

