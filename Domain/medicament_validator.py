from Domain.medicament import Medicament


class MedicamentValidator:
    def validate(self, medicament: Medicament):
        errors = []
        if medicament.pret < 0:
            errors.append("Pretul trebuie sa fie strict pozitiv")

        if errors:
            raise ValueError(errors)
