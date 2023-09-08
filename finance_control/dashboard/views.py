from django.shortcuts import render
from django.db.models import Sum, F, Case, When, Value, DecimalField

from .models import Person, TransactionLog, PersonBank

# Create your views here.


def index(request):
    context = {}
    template_name = 'dashboard/index.html'

    total_sum = (
        TransactionLog.objects
        .filter(credit_card__isnull=True)
        .annotate(
            total_value=Sum(
                Case(
                    When(type='saida', then=F('value') * Value(-1)),
                    default='value',
                    output_field=DecimalField()
                )
            )
        )
        .aggregate(total=Sum('total_value'))
    )

    transactions = TransactionLog.objects.all()

    savio = Person.objects.get(person="Sávio")
    tay = Person.objects.get(person="Tay")

    person_banks_s = PersonBank.objects.filter(person_associated=savio)
    person_banks_t = PersonBank.objects.filter(person_associated=tay)

    context['total_sum'] = total_sum['total']
    context['transactions'] = transactions
    context['person_banks_s'] = person_banks_s
    context['person_banks_t'] = person_banks_t

    return render(request, template_name, context)
