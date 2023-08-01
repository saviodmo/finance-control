from django.shortcuts import render

# Create your views here.


def index(request):
    context = {}
    template_name = 'dashboard/index.html'

    context['data'] = [1, 2, 3, 4, 5]
    return render(request, template_name, context)
