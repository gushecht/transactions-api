from django.db.models import Count, Sum
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
import json

from .models import Payins, Payouts


def duplicates(request):
    if request.method == 'GET':
        filter_params = {
            'timestamp__gte': request.GET.get('from'),
            'timestamp__lt': request.GET.get('to')
        }

        payouts = list(Payouts.objects.filter(**filter_params).values('transaction_id').annotate(total=Count('transaction_id')))

        transactions_with_duplicated_payouts = [t.get('transaction_id') for t in filter(lambda p: p.get('total') > 1, payouts)]

        return JsonResponse({'transactions': transactions_with_duplicated_payouts})

    return HttpResponseNotAllowed(['GET'])


def payin(request):
    if request.method == 'POST':
        Payins.objects.create_payin(**json.loads(request.body))

        return HttpResponse()

    return HttpResponseNotAllowed(['POST'])


def payout(request):
    if request.method == 'POST':
        Payouts.objects.create_payout(**json.loads(request.body))

        return HttpResponse()

    return HttpResponseNotAllowed(['POST'])


def revenue(request):
    if request.method == 'GET':
        filter_params = {
            'timestamp__gte': request.GET.get('from'),
            'timestamp__lt': request.GET.get('to')
        }

        payins = Payins.objects.filter(**filter_params).aggregate(Sum('amount')).get('amount__sum', 0.0)
        payouts = Payouts.objects.filter(**filter_params).aggregate(Sum('amount')).get('amount__sum', 0.0)

        return JsonResponse({'revenue': round(payins - payouts, 2)})

    return HttpResponseNotAllowed(['GET'])


def transactions(request, transaction_id: int):
    if request.method == 'GET':
        filter_params = {'transaction_id__exact': transaction_id}

        payins = Payins.objects.filter(**filter_params).values('amount', 'timestamp')
        payouts = Payouts.objects.filter(**filter_params).values('amount', 'timestamp')

        return JsonResponse({'payins': list(payins), 'payouts': list(payouts)})

    return HttpResponseNotAllowed(['GET'])
