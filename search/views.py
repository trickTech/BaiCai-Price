from django.http import HttpResponse, JsonResponse
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
import datetime
from search.models import Vegetable, Record
from django.core.exceptions import ObjectDoesNotExist


def cross_site(func):
    def add_cross_site(*args, **kwargs):
        response = func(*args, **kwargs)
        if isinstance(response, HttpResponse):
            response["Access-Control-Allow-Origin"] = "*"
            response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"

        return response

    return add_cross_site


# Create your views here.
@cross_site
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


@cross_site
def today(request):
    record_list = Record.objects.filter(created_at__day=datetime.date.today().day)
    record_list = [v.as_dict() for v in record_list]

    records = create_pageinator(request, record_list)

    if not records:
        return JsonResponse([], safe=False)
    else:
        return JsonResponse(records, safe=False)


@cross_site
def vegetable_history(request, veg_id):
    vegetable = None

    try:
        vegetable = Vegetable.objects.get(pk=veg_id)
        record = vegetable.record_set.all()
    except ObjectDoesNotExist:
        return JsonResponse([], safe=False)

    record = [v.as_dict() for v in record]

    return JsonResponse(record, safe=False)
