from django.db import models
from django.db.models import signals
from django.urls import reverse


class Category(models.Model):
    dtt_record = models.DateTimeField("Data de Inserção", auto_now_add=True, blank=True)
    category = models.CharField("Categoria", max_length=200)
    description = models.CharField("Descrição", max_length=200)

    objects = models.Manager()

    def __str__(self):
        return self.category


class Person(models.Model):
    dtt_record = models.DateTimeField("Data de Inserção", auto_now_add=True, blank=True)
    person = models.CharField("Pessoa", max_length=50)
    slug = models.SlugField('Slug', max_length=255, blank=True, null=True, unique=True)

    objects = models.Manager()

    def __str__(self):
        return self.person

    def get_absolute_url(self):
        return reverse('dashboard:pessoa', args=[self.slug])

    def all_banks(self):
        return self.person_banks.all()


class Bank(models.Model):
    dtt_record = models.DateTimeField("Data de Inserção", auto_now_add=True, blank=True)
    bank = models.CharField("Banco", max_length=50)

    objects = models.Manager()

    def __str__(self):
        return self.bank

    def all_transaction(self):
        return self.transactions.all()


class CreditCard(models.Model):
    dtt_record = models.DateTimeField("Data de Inserção", auto_now_add=True, blank=True)
    card = models.CharField("Cartão", max_length=50)
    flag = models.CharField("Bandeira", max_length=50)
    limit = models.DecimalField("Limite", max_digits=10, decimal_places=2)
    bank = models.ForeignKey(Bank, related_name='credit_cards', on_delete=models.PROTECT)
    person = models.ForeignKey(Person, related_name='credit_cards', on_delete=models.PROTECT)
    due_date = models.IntegerField("Data de Vencimento")

    objects = models.Manager()

    def __str__(self):
        return self.card


class TransactionLog(models.Model):
    dtt_record = models.DateTimeField("Data de Inserção", auto_now_add=True, blank=True)
    dt_transaction = models.DateField("Data da Transação")
    description = models.CharField("Descrição", max_length=200)
    expense_category = models.ForeignKey(Category, related_name='transactions', on_delete=models.PROTECT)
    val_transaction = models.DecimalField("Valor", max_digits=10, decimal_places=2)
    transaction_bank = models.ForeignKey(Bank, related_name='transactions', on_delete=models.PROTECT)

    TRANSACTION_TYPE_CHOICES = (
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    )
    type = models.CharField("Tipo de transação", max_length=10, choices=TRANSACTION_TYPE_CHOICES)

    transaction_person = models.ForeignKey(Person, related_name='transactions', on_delete=models.PROTECT)
    observation = models.CharField("Observação", max_length=200)
    credit_card = models.ForeignKey(CreditCard, related_name="transactions", on_delete=models.PROTECT,
                                    null=True, blank=True, default=None)

    objects = models.Manager()

    def val_calculate(self):
        entrada = 0
        if self.type == 'entrada':
            entrada = sum(self.val_transaction)

        saida = 0
        if self.type == 'saida':
            saida = sum(self.val_transaction)

        return entrada - saida


class FixedExpenses(models.Model):
    dtt_record = models.DateTimeField("Data de Inserção", auto_now_add=True, blank=True)
    description = models.CharField("Descrição", max_length=200)
    value = models.DecimalField("Valor", max_digits=10, decimal_places=2)
    due_date = models.IntegerField("Data de Vencimento")

    TYPE_CHOICES = (
        ('credito', 'Crédito'),
        ('debito', 'Débito'),
    )
    type = models.CharField("Tipo", max_length=10, choices=TYPE_CHOICES)

    STATUS_CHOICES = (
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
    )
    status = models.CharField("Status", max_length=10, choices=STATUS_CHOICES, default='ativo')

    objects = models.Manager()


class PersonBank(models.Model):
    dtt_record = models.DateTimeField("Data de Inserção", auto_now_add=True, blank=True)
    bank_associated = models.ForeignKey(Bank, related_name='person_banks', on_delete=models.PROTECT)
    person_associated = models.ForeignKey(Person, related_name='person_banks', on_delete=models.PROTECT)

    objects = models.Manager()


from libs.signals import slug_pre_save
signals.pre_save.connect(slug_pre_save, sender=Person)

