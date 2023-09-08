from django.contrib import admin

from .models import Category, Bank, Person, CreditCard, TransactionLog, FixedExpenses, PersonBank


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category', 'description']


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ['bank']


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['person']


@admin.register(CreditCard)
class CreditCardAdmin(admin.ModelAdmin):
    list_display = ['card', 'flag', 'limit', 'bank', 'person', 'due_date']


@admin.register(TransactionLog)
class TransactionLogAdmin(admin.ModelAdmin):
    list_display = ['dt_transaction', 'description', 'expense_category', 'value', 'transaction_bank', 'type',
                    'transaction_person', 'observation', 'credit_card']


@admin.register(FixedExpenses)
class FixedExpensesAdmin(admin.ModelAdmin):
    list_display = ['description', 'value', 'due_date', 'type', 'status']


@admin.register(PersonBank)
class PersonBankAdmin(admin.ModelAdmin):
    list_display = ['bank_associated', 'person_associated']
