from django.http import HttpResponse, JsonResponse
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
import datetime
from search.models import Item, Record
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max


def order_by(request, query):
    attribute = request.GET.get('order_by')
    reversed = request.GET.get('reversed')

    if attribute:
        if reversed and reversed.lower() == 'true':
            attribute = '-' + attribute
        try:
            query = query.order_by(attribute)
        except Exception:
            pass
    else:
        return query

    return query


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

    response = {
        'total_page': paginator.num_pages,
        'element_per_page': per_page
    }

    response['content'] = record.object_list

    return response


@cross_site
def today(request):
    record_list = Record.objects.filter(created_at__day=datetime.date.today().day)
    record_list = order_by(request, record_list)
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
        vegetable = Item.objects.get(pk=veg_id)
        record = vegetable.record_set.all()
        record = order_by(request, record)
    except ObjectDoesNotExist:
        return JsonResponse([], safe=False)

    record = [v.as_dict() for v in record]

    record = create_pageinator(request, record)

    return JsonResponse(record, safe=False)


@cross_site
def search(request):
    slug = request.POST.get('veg_name')
    records = Record.objects.raw(
        'select * from search_record where veg_name like %s group by vegetable_id order by created_at',
        ['%{}%'.format(slug)])
    records = [i.as_dict() for i in records]
    records = create_pageinator(request, records)

    return JsonResponse(records, safe=False)


@cross_site
def record_history(request, date):
    try:
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'status': -1, 'error': '日期格式有误'})

    records = Record.objects.filter(created_at=date).all()
    records = [i.as_dict() for i in records]
    records = create_pageinator(request, records)

    return JsonResponse(records, safe=False)
