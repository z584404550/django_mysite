from django.contrib.contenttypes.models import ContentType
from .models import ReadNum


def read_statistics_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = '%s_%s_read' % (ct.model, obj.pk)

    if not request.COOKIES.get(key):
        # 存在记录
        if ReadNum.objects.filter(content_type=ct, object_id=obj.pk).count():
            read_num = ReadNum.objects.get(content_type=ct, object_id=obj.pk)
        # 不存在记录
        else:
            read_num = ReadNum(content_type=ct, object_id=obj.pk)
        # 计数+1
        read_num.read_num += 1
        read_num.save()
    return key
