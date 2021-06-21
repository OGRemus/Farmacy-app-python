
import csv
from Repo.file_repository import FileRepository


class ExportExcel:

    @staticmethod
    def write(meds):
        with open("Medicamente.csv", "w") as _:
            pass
        for medicament in meds:
            row = [str(medicament.id_entitate), str(medicament.nume), str(medicament.pret),
               str(medicament.producator), str(medicament.reteta)]

            with open("Medicamente.csv", 'a', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(row)


