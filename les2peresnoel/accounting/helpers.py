# import pandas as pd
from django.db.transaction import atomic as atomic_transaction
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .models import Account, ChartOfAccount, Transaction, JournalEntry, Journal


# def import_accounts_from_excel(file_path, coa=None):
#     breakpoint()
#     # Lire le fichier Excel
#     df = pd.read_excel(file_path, engine='openpyxl')
#     # coa_pk = coa.pk if coa else None
#     # Affiche les premières lignes pour vérifier
#     # print(df.head())

#     # Vérifiez et renommez les colonnes si nécessaire
#     if 'code' not in df.columns or 'name' not in df.columns:
#         df.columns = ['code', 'name']  # Renommez les colonnes si elles ne sont pas correctement nommées

#     # Nettoyer les données et remplir les colonnes manquantes
#     df = df[['code', 'name']].dropna()
#     df['code'] = df['code'].astype(str)
#     df['parent_code'] = df['code'].apply(lambda x: x[:-1] if len(x) > 1 else None)

#     # Création des comptes
#     with atomic_transaction(using='default'):
#         for _, row in df.iterrows():
#             code = str(row['code']).strip()
#             name = row['name'].strip()
#             parent_code = str(row['parent_code']).strip() if 'parent_code' in row and not pd.isna(
#                 row['parent_code']) else None

#             parent = Account.objects.filter(code=parent_code, coa=coa).first() if parent_code else None

#             account, created = Account.objects.update_or_create(
#                 code=code, coa=coa,
#                 defaults={'name': name, 'parent': parent}
#             )
#             # print(f"{parent_code} -> {code} --> {name}")

try:
    coa, created = ChartOfAccount.objects.get_or_create(name="default", description=_("Plan comptable par défaut"))
    CUSTOMER_ACCOUNTS_RECEIVABLE, created = Account.objects.get_or_create(
        code=settings.BASE_ACCOUNT_CODE_MAP['CUSTOMER_ACCOUNTS_RECEIVABLE'], coa=coa, name=_("Créance client"))
    BANK, created = Account.objects.get_or_create(
        code=settings.BASE_ACCOUNT_CODE_MAP['BANK'], coa=coa, name=_("Banque"))
    BORROWINGS_FROM_CREDIT_INSTITUTIONS, created = Account.objects.get_or_create(
        code=settings.BASE_ACCOUNT_CODE_MAP['BORROWINGS_FROM_CREDIT_INSTITUTIONS'], coa=coa, name=_(
            "Emprunts auprès d'établissements de crédit"))
    INTEREST_CHARGES, created = Account.objects.get_or_create(code=settings.BASE_ACCOUNT_CODE_MAP['INTEREST_CHARGES'],
                                                            coa=coa,
                                                            name=_("Charges d'intérêt"))
    CAPITAL, created = Account.objects.get_or_create(code=settings.BASE_ACCOUNT_CODE_MAP['CAPITAL'], coa=coa,
                                                    name=_("Capital"))
    RAW_MATERIALS_PURCHASES, created = Account.objects.get_or_create(
        code=settings.BASE_ACCOUNT_CODE_MAP['RAW_MATERIALS_PURCHASES'], coa=coa,
        name=_("Achats de matières premières"))
    INDUSTRIAL_EQUIPMENT, created = Account.objects.get_or_create(
        code=settings.BASE_ACCOUNT_CODE_MAP['INDUSTRIAL_EQUIPMENT'],
        coa=coa, name=_("Matériel industriel"))
    SALES_OF_FINISHED_PRODUCTS, created = Account.objects.get_or_create(
        code=settings.BASE_ACCOUNT_CODE_MAP['SALES_OF_FINISHED_PRODUCTS'], coa=coa,
        name=_("Ventes de produits finis"))
    SUPPLIER_DEBT, created = Account.objects.get_or_create(code=settings.BASE_ACCOUNT_CODE_MAP['SUPPLIER_DEBT'], coa=coa,
                                                        name=_("Dette fournisseur"))

    SALES_COMMISSIONS, created = Account.objects.get_or_create(
        code=settings.BASE_ACCOUNT_CODE_MAP['SALES_COMMISSIONS'], coa=coa, name=_("Commissions de vente"))


except Exception as e:
    ...


def transaction_accounting(transaction: Transaction):
    with atomic_transaction(using='default'):
        default_journal, created = Journal.objects.get_or_create(name="default",
                                                                 description=_(
                                                                      "Journal de transaction par défaut"),
                                                                 #  business_date=self.business_date
                                                                 )
        debit_entry = JournalEntry.objects.create(
            name=f"DEBIT - {transaction.debit_account.name}",
            transaction=transaction,
            entry_type=JournalEntry.EntryType.DEBIT,
            account=transaction.debit_account,
            amount=transaction.amount,
            description=transaction.description
        )
        credit_entry = JournalEntry.objects.create(
            name=f"CREDIT - {transaction.credit_account.name}",
            transaction=transaction,
            entry_type=JournalEntry.EntryType.CREDIT,
            account=transaction.credit_account,
            amount=transaction.amount,
            description=transaction.description
        )
        # debit_entry.save()
        # credit_entry.save()

        debit_entry.journals.add(default_journal)
        credit_entry.journals.add(default_journal)

def process_accounting_for_customer_order(amount, description: str = None):
    # Todo:: create a class that order models will extend to ensure that we have a consistent interface
    # New order means that the customer must pay some amount
    try:
        with atomic_transaction(using='default'):
            # Save customer order 
            transaction = Transaction.objects.create(
                debit_account=CUSTOMER_ACCOUNTS_RECEIVABLE,
                credit_account=SALES_OF_FINISHED_PRODUCTS,
                amount=amount,
                description=description,
            )
            transaction_accounting(transaction)
    except Exception as e:
        raise e


def process_payment_accounting(amount, description: str = None):
    try:
        with atomic_transaction(using='default'):
            # Register the advance
            transaction=Transaction.objects.create(
                debit_account=BANK,
                credit_account=CUSTOMER_ACCOUNTS_RECEIVABLE,
                amount=amount,
                description=description or _("Avance")
            )
            transaction_accounting(transaction)
    except Exception as e:
        raise e


def process_commissions_accounting(amount, description: str = None):
    try:
        with atomic_transaction(using='default'):
            transaction = Transaction.objects.create(
                debit_account=SALES_COMMISSIONS,
                credit_account=BANK,
                amount=amount,
                description=description or _("Prélèvement de la commission de vente")
            )
            transaction_accounting(transaction)
    except Exception as e:
        raise e


def process_supplier_accounting(amount, description):
    try:
        with atomic_transaction(using='default'):
            transaction = Transaction.objects.create(
                debit_account=SUPPLIER_DEBT,
                credit_account=BANK,
                amount=amount,
                description=description or _("Reversement au fournisseurs")
            )
            transaction_accounting(transaction) 
    except Exception as e:
        raise e
