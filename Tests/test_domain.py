from Domain.card_client import CardClient
from Domain.medicament import Medicament
from Domain.tranzactie import Tranzactie


def test_domain():
    m = Medicament("1", "paracetamol", "prod", 100, "NU")
    c = CardClient("1","ion","pelea","1231231231","1.nov.1980", "10.oct.2019")
    t = Tranzactie("1", "1", "1", 10, "10.10.2020, 3.23.40", 1000, 10)

    assert m.id_entitate == "1"
    assert m.nume == "paracetamol"
    assert m.producator == "prod"
    assert m.pret == 100
    assert m.reteta == "NU"

    assert c.id_entitate == "1"
    assert c.nume == "ion"
    assert c.prenume == "pelea"
    assert c.CNP == "1231231231"
    assert c.data_nastere == "1.nov.1980"
    assert c.data_inregistrare == "10.oct.2019"

    assert t.id_entitate == "1"
    assert t.id_medicament == "1"
    assert t.id_card_client == "1"
    assert t.nr_bucati == 10
    assert t.data_ora == "10.10.2020, 3.23.40"
    assert t.pret == 1000
    assert t.reducere == 10


test_domain()