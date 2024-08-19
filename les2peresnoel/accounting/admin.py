from django.contrib import admin
from .models import Account, Journal, JournalEntry, Transaction, BusinessDate
# Register your models here.

admin.site.register(Account)
admin.site.register(Journal)
admin.site.register(JournalEntry)
admin.site.register(Transaction)
admin.site.register(BusinessDate)