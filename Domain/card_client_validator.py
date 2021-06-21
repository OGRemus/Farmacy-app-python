from datetime import datetime

from Domain.card_client import CardClient


class CardClientValidator:

    def validate(self, card_client: CardClient):
        errors = []
        try:
            variable = datetime.strptime(card_client.data_inregistrare, "%d.%b.%Y").date()
            variable2 = datetime.strptime(card_client.data_nastere, "%d.%b.%Y").date()
        except ValueError as e:
            errors.append(e)

        if errors:
            raise ValueError(errors)