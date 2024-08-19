from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum
from model_utils.models import TimeStampedModel
from django.db.transaction import atomic as atomic_transaction
from .exceptions import JournalCloseException, JournalEntryException
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class BusinessDate(TimeStampedModel):
    class Meta:
        verbose_name = _('Journée comptable')
        verbose_name_plural = _('Journées comptables')
    date = models.DateField()
    open = models.BooleanField(default=True)

    def __str__(self):
        return str(self.date)

    @classmethod
    def can_open_next(cls):
        return not BusinessDate.objects.filter(open=True).exists()

    def approve_business_date_entry(self):
        JournalEntry.objects.filter(business_date=self).update(approved=True)

    @classmethod
    def get_open_business_date(cls):
        try:
            return BusinessDate.objects.get(open=True)
        except BusinessDate.DoesNotExist:
            return None

    def close_business_date(self):
        # Check if all debit is equal to credit
        # Check if all credit is equal to debit
        # Approve JournalEntry
        # Close business date
        # Create new business date
        with atomic_transaction(using='default'):
            debits = JournalEntry.objects.filter(entry_type=JournalEntry.EntryType.DEBIT, business_date=self)
            credits = JournalEntry.objects.filter(entry_type=JournalEntry.EntryType.CREDIT, business_date=self)
            debits_balance = debits.aggregate(Sum('amount')).get(
                'amount__sum') or 0
            credits_balance = credits.aggregate(Sum('amount')).get(
                'amount__sum') or 0

            if debits_balance == credits_balance:
                self.approve_business_date_entry()
                self.open = False
                self.save()
                if BusinessDate.can_open_next():
                    new_business_date = BusinessDate(date=self.date.day + 1, open=True)
                    new_business_date.save()
            else:
                raise JournalCloseException(debits_balance, credits_balance)


# Create your models here.
class ChartOfAccount(models.Model):
    class Meta:
        verbose_name = _('Plan comptable')
        verbose_name_plural = _('Plan comptables')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    default = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.default:
            ChartOfAccount.objects.filter(default=True).update(default=False)
        super().save(*args, **kwargs)

    # Todo : Rewrite delete


class Account(models.Model):
    class Meta:
        verbose_name = _('Compte')
        verbose_name_plural = _('Comptes')
    coa = models.ForeignKey(ChartOfAccount, on_delete=models.CASCADE)
    code = models.CharField(max_length=50, unique=True, db_index=True)
    name = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    # node_order_by = ['code']
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    def __str__(self):
        return f"{self.code} - {self.name}"

    @property
    def credits_balance(self):
        return JournalEntry.objects.filter(entry_type=JournalEntry.EntryType.CREDIT, account=self).aggregate(
            Sum('amount')).get('amount__sum') or 0

    @property
    def debits_balance(self):
        return JournalEntry.objects.filter(entry_type=JournalEntry.EntryType.DEBIT, account=self).aggregate(
            Sum('amount')).get('amount__sum') or 0

    @property
    def get_balance(self):
        return abs(self.credits_balance - self.debits_balance)

    def save(self, *args, **kwargs):
        self.balance = self.get_balance
        super().save(*args, **kwargs)


class Transaction(TimeStampedModel):
    class Meta:
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')
    debit_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='debit_entries')
    credit_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='credit_entries')
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.debit_account} --> {self.credit_account} : {self.amount} ({self.description})"

    # def save(self, *args, **kwargs):
    #     if self._state.adding:
    #             # self.journals.add(default_journal)
    #             super().save(*args, **kwargs)


class Journal(TimeStampedModel):
    class Meta:
        verbose_name = _('Journal')
        verbose_name_plural = _('Journaux')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class JournalEntry(TimeStampedModel):
    class Meta:
        verbose_name = _('Entrée de journal')
        verbose_name_plural = _('Entrées de journal')
    class EntryType(models.TextChoices):
        DEBIT = 'debit', _('Debit')
        CREDIT = 'credit', _('Credit')

    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='entries')
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.SET_NULL, null=True, related_name='entries')
    entry_type = models.CharField(max_length=6, choices=EntryType.choices)
    journals = models.ManyToManyField(Journal, related_name="entries")
    business_date = models.ForeignKey(BusinessDate, on_delete=models.DO_NOTHING, null=True)
    approved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        business_date = BusinessDate.get_open_business_date()
        if business_date:
            self.business_date = business_date
        else:
            raise JournalEntryException("No open business date")
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.entry_type} - {self.amount} - {self.account}"
