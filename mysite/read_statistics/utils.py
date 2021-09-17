import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from .models import ReadNum, ReadDetail


def read_statistics_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = '%s_%s_read' % (ct.model, obj.pk)

    if not request.COOKIES.get(key):
        # # 存在记录
        # if ReadNum.objects.filter(content_type=ct, object_id=obj.pk).count():
        #     read_num = ReadNum.objects.get(content_type=ct, object_id=obj.pk)
        # # 不存在记录
        # else:
        #     read_num = ReadNum(content_type=ct, object_id=obj.pk)
        # # 计数+1
        read_num, created = ReadNum.objects.get_or_create(
            content_type=ct, object_id=obj.pk)
        read_num.read_num += 1
        read_num.save()
        # 当天阅读数
        date = timezone.now().date()
        # if ReadDetail.objects.filter(content_type=ct, object_id=obj.pk, date=date).count():
        #     read_detail = ReadDetail.objects.get(content_type=ct, object_id=obj.pk, date=date)
        #     # 不存在记录
        # else:
        #     read_detail = ReadDetail(content_type=ct, object_id=obj.pk,date=date)
        #     # 计数+1
        read_detail, created = ReadDetail.objects.get_or_create(
            content_type=ct, object_id=obj.pk, date=date)
        read_detail.read_num += 1
        read_detail.save()
    return key


def get_seven_days_read_data(content_type):
    today = timezone.now().date()
    dates = list()
    read_nums = list()
    for i in range(7, 0, -1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        read_details = ReadDetail.objects.filter(
            content_type=content_type, date=date)
        result = read_details.aggregate(read_num_sum=Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0)
    return dates, read_nums


def get_today_hot_data(content_type):
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(
        content_type=content_type, date=today).order_by('-read_num')
    return read_details[:7]


def get_yesterday_hot_data(content_type):
    today = timezone.now().date()
    date = today - datetime.timedelta(days=1)
    read_details = ReadDetail.objects.filter(
        content_type=content_type, date=date).order_by('-read_num')
    return read_details[:7]
