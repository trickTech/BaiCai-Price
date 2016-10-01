from django.http import HttpResponse, JsonResponse
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
import datetime
from search.models import Vegetable, Record
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def create_pageinator(request, record_list, per_page=15):
    paginator = Paginator(record_list, per_page)
    page = request.GET.get('page')
    try:
        record = paginator.page(page)
    except PageNotAnInteger:
        record = paginator.page(1)
    except EmptyPage:
        record = paginator.page(paginator.num_pages)
    return record.object_list


def today(request):
    record_list = Record.objects.filter(created_at__day=datetime.date.today().day)
    record_list = [v.as_dict() for v in record_list]

    records = create_pageinator(request, record_list)

    return JsonResponse(records, safe=False)


def vegetable_history(request, veg_id):
    vegetable = None

    try:
        vegetable = Vegetable.objects.get(pk=veg_id)
        record = vegetable.record_set.all()
    except ObjectDoesNotExist:
        return JsonResponse([])

    

    record = [v.as_dict() for v in record]

    return JsonResponse(record, safe=False)
