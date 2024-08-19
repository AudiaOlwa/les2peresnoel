class JournalCloseException(Exception):
    def __init__(self, debit, credit):
        self.debit = debit
        self.credit = credit
        self.difference = abs(debit - credit)
        super().__init__(
            f"Echec de la fermeture de la journée comptable. Solde débit: {debit}, Solde crédit: {credit}, Écart: {self.difference}")


class JournalEntryException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(f"{message}")
