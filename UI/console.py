from datetime import datetime

from Domain.medicament import Medicament
from Exceptions.invalid_card_exception import InvalidCardException
from Exceptions.medicament_exception import InvalidMedicamentException
from Exceptions.undoredo_exception import UndoRedoException
from Repo.ExportExcel import ExportExcel
from Service.UndoRedoService import UndoRedoService
from Service.card_client_service import CardClientService
from Service.medicament_service import MedicamentService
from Service.tranzactie_service import TranzactieService


class Console:

    def __init__(self,
                 medicament_service: MedicamentService,
                 card_client_service: CardClientService,
                 tranzactie_service: TranzactieService,
                 undo_redo_service: UndoRedoService,

                 ):
        self.__undo_redo_service = undo_redo_service

        self.__medicament_service = medicament_service
        self.__card_client_service = card_client_service
        self.__tranzactie_service = tranzactie_service

    def print_menu(self):
        print("\n")
        print("1.CRUD Medicamente")
        print("2.CRUD Card client")
        print("3.CRUD Tranzactii")
        print("4.Functionalitati")
        print("5.Undo")
        print("6.Redo")
        print("x.Iesire")

    def run_console(self):
        while True:
            self.print_menu()
            optiune = input("Alegeti optiunea ")
            if optiune == "1":
                self.run_crud_medicamente()
            elif optiune == "2":
                self.run_crud_card_client()
            elif optiune == "3":
                self.run_crud_tranzactii()
            elif optiune == "4":
                self.run_functionalitati()
            elif optiune == "5":
                try:
                    self.__undo_redo_service.do_undo()
                except UndoRedoException as ure:
                    print(ure.message)
            elif optiune == "6":
                try:
                    self.__undo_redo_service.do_redo()
                except UndoRedoException as ure:
                    print(ure.message)
            elif optiune == "x":
                break
            else:
                print("Optiunea este invalida!")

    def run_crud_medicamente(self):
        while True:
            print("\n")
            print("1.Creeaza medicament ")
            print("2.Sterge medicament ")
            print("3.Actualizeaza medicament ")
            print("a.Afiseaza medicamente")
            print("b.Back")
            optiune = input("Alegeti optiunea ")
            if optiune == "1":
                self.handle_create_medicament()
                self.__undo_redo_service.clear_redo()
            elif optiune == "2":
                self.handle_sterge_medicament()
                self.__undo_redo_service.clear_redo()
            elif optiune == "3":
                self.handle_actualizeaza_medicament()
                self.__undo_redo_service.clear_redo()
            elif optiune == "a":
                self.handle_show_all_medicamente()
            elif optiune == "b":
                break
            else:
                print("Optiunea este invalida !")

    def handle_create_medicament(self):
        try:
            id_medicament = input("ID-ul medicamentului: ")
            nume = input("Numele medicamentului: ")
            producator = input("Producatorul medicamentului: ")
            pret = int(input("Pretul medicamentului: "))
            reteta = input("Necesita reteta?(DA/NU) ")
            self.__medicament_service.create(id_medicament, nume, producator, pret, reteta)

        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def handle_show_all_medicamente(self):
        for medicament in self.__medicament_service.get_all():
            print(medicament)

    def handle_sterge_medicament(self):
        try:
            id_medicament = input("Oferiti id-ul medicamentului de sters : ")
            self.__medicament_service.delete(id_medicament)
            self.__tranzactie_service.delete_all_tranzactii_medicament(id_medicament)
            print("Medicamentul a fost sters ")
        except KeyError as ke:
            print(ke)
        except InvalidMedicamentException as e:
            print(e)

    def handle_actualizeaza_medicament(self):
        try:
            id_medicament = input("Oferiti id-ul medicamentuluui de actualizat ")
            nume = input("Oferti numele medicamentului ")
            pret = int(input("Oferiti pretul medicamentului "))
            producator = input("Oferiti producatorul medicamentului ")
            reteta = input("Medicamentul are nevoie de reteta(DA/NU) ")
            self.__medicament_service.update(id_medicament, nume, producator, pret, reteta)
        except KeyError as v:
            print(v)

    def run_crud_card_client(self):
        while True:
            print("\n")
            print("1.Creeaza card client")
            print("2.Sterge card client")
            print("3.Actualizeaza card client")
            print("a.Afisare card client")
            print("x.Iesire")
            optiune = input("Alegeti o optiune ")
            if optiune == "1":
                self.handle_create_card()
            if optiune == "2":
                self.handle_sterge_card()
            if optiune == "3":
                self.handle_update_card()
            if optiune == "a":
                self.handle_show_all_card()
            if optiune == "x":
                break

    def handle_create_card(self):
        try:
            id_card = input("ID-ul cardului: ")
            nume = input("Numele clientului : ")
            prenume = input("Prenumele clientului: ")
            try:
                cnp = int(input("CNP-ul clientului: "))
                data_nastere = input("Data de nastere a clientului: ")
                data_inregistrare = input("Data inregistrare a clientului")
                self.__card_client_service.create(id_card, nume, prenume, cnp, data_nastere, data_inregistrare)
            except ValueError:

                print("Cnpul trebuie sa fie int")

        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def handle_sterge_card(self):
        try:
            id_card = input("Oferiti id-ul cardului de sters")
            self.__card_client_service.delete(id_card)
        except ValueError as v:
            print(v)

    def handle_update_card(self):

        try:
            id_card = input("Oferiti id-ul cardului de actualizat ")
            nume = input("Numele clientului : ")
            prenume = input("Prenumele clientului: ")
            cnp = int(input("CNP-ul clientului: "))
            data_nastere = input("Data de nastere a clientului:FORMAT 10.dec.2020 ")
            data_inregistrare = input("Data inregistrare a clientului FORMAT 10.dec.2020")
            self.__card_client_service.update(id_card, nume, prenume, cnp, data_nastere, data_inregistrare)
        except ValueError:
            print("Cnp ul trebuie sa fie int")

    def handle_show_all_card(self):
        for card in self.__card_client_service.get_all():
            print(card)

    def run_crud_tranzactii(self):
        while True:
            print("\n")
            print("1.Creeaza tranzactie")
            print("2.Sterge tranzactie")
            print("3.Actualizeaza tranzactie")
            print("a.Afiseaza tranzactii")
            print("x.Iesire")

            optiune = input("Alegeti o optiune ")

            if optiune == "1":
                self.handle_adauga_tranzactie()
            elif optiune == "2":
                self.handle_sterge_tranzactie()
            elif optiune == "3":
                self.handle_update_tranzactie()
            elif optiune == "a":
                self.handle_show_tranzactii()
            elif optiune == "x":
                break

    def handle_adauga_tranzactie(self):
        try:
            id_tranzactie = input("Id-ul tranzactiei ")
            id_medicament = input("Id-ul medicamentului")
            id_card = input("Id-ul cardului de client")
            nr_bucati = int(input("Numarul de bucati cumparate "))
            data_ora = input("Data si ora tranzactiei FORMAT 10.oct.2020,10.10.10")
            try:
                data = datetime.strptime(data_ora, "%d.%b.%Y,%H.%M.%S")
                self.__tranzactie_service.create(id_tranzactie, id_medicament, id_card, nr_bucati, data)
            except ValueError as ke:
                print(ke)
            except KeyError as e:
                print(e)
        except ValueError as ve:
            print(ve)
        except KeyError as ke2:
            print(ke2)
        except Exception as e:
            print(e)

    def handle_sterge_tranzactie(self):
        id_tranzactie = input("Oferiti id-ul tranzactiei de sters ")
        self.__tranzactie_service.delete(id_tranzactie)

    def handle_update_tranzactie(self):
        try:
            id_tranzactie = input("Id-ul tranzactiei ")
            id_medicament = input("Id-ul medicamentului")
            id_card = input("Id-ul cardului de client")
            nr_bucati = int(input("Numarul de bucati cumparate "))
            data_ora = input("Data si ora tranzactiei FORMAT 10.oct.2020,10.10.10")
            data_ora = datetime.strptime(data_ora, "%d.%b.%Y,%H.%M.%S")

            self.__tranzactie_service.update(id_tranzactie, id_medicament, id_card, nr_bucati, data_ora)
        except ValueError as ve:
            print(ve)
        except KeyError as ke2:
            print(ke2)
        except InvalidCardException as e:
            print(e)
        except Exception as e:
            print(e)

    def handle_show_tranzactii(self):
        for tranzactie in self.__tranzactie_service.get_all():
            print(tranzactie)

    def run_functionalitati(self):
        while True:
            print("\n")
            print("1.Scumpire medicamente")
            print("2.Populeaza entitati: ")
            print("3.Afisarea tranzactiilor dintr-un interval de timp: ")
            print("4.Stergerea tranzactiilor dintr-un interval de timp: ")
            print("5.Afisarea medicamentelor descrescator dupa numarul de vanzari ")
            print("6.Afisarea cardurilor descrescator dupa valoarea de reduceri obtinute ")
            print("7.Cautare ")
            print("x.Iesire")

            optiune = input("Alegeti o opitune")
            if optiune == "1":
                try:
                    valoare = int(input("Oferiti valoarea de comparat pretul"))
                    procent = int(input("Oferiti procentul de scumpire"))
                    self.__medicament_service.scumpire(valoare, procent)
                except ValueError:
                    print("Valorile trebuie sa fie int")
            elif optiune == "2":
                n = int(input("Oferiti nr entitati"))
                self.__medicament_service.populate_entities(n)
            elif optiune == "3":
                var1 = input("Oferiti data de start in format zz.ll.aa")
                var2 = input("Oferiti data final in format zz.ll.aa")
                try:

                    start_date = datetime.strptime(var1, "%d.%b.%Y").date()
                    finish_date = datetime.strptime(var2, "%d.%b.%Y").date()

                    print(self.__tranzactie_service.tranzactii_pe_interval(start_date, finish_date))
                except ValueError as e:
                    print(e)
            elif optiune == "4":
                var1 = input("Oferiti data de start in format zz.ll.aa")
                var2 = input("Oferiti data final in format zz.ll.aa")
                try:
                    start_date = datetime.strptime(var1, "%d.%b.%Y").date()
                    finish_date = datetime.strptime(var2, "%d.%b.%Y").date()
                    self.__tranzactie_service.stergere_tranzactii_pe_interval(start_date, finish_date)
                except ValueError as e:
                    print(e)
            elif optiune == "5":
                print("Medicamentele sorate descrescator dupa numarul de vanzari :",
                      self.__tranzactie_service.medicamente_nr_vanzari())
            elif optiune == "6":
                print("Cardurile ordonate descrescator dupa valoarea reducerilor (id : valoare) ", self.__tranzactie_service.ordoneaza_card_client_dupa_reduceri())
            elif optiune == "7":
                cautare = input("Cautare medicamente/carduri (alege) ")
                if cautare == "medicamente":
                    tip = input("Ofertiti tipul de cautare : nume/producator/pret/reteta/text ").lower()
                    var = input("Introduceti ce doriti sa cautati ")
                    print(self.__medicament_service.cautare(tip, var))

                elif cautare == "carduri":
                    tip = input("Oferiti tipul de cautare : nume/prenume/CNP/data nastere/data inregistrare/text: ").lower()
                    var = input("Oferiti valoarea de cautat ")
                    print(self.__card_client_service.cautare(tip, var))

            elif optiune == "x":
                break
