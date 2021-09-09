from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import ReadNum


register = template.Library()


@register.simple_tag
def get_read_num(obj):
    content_type = ContentType.objects.get_for_model(obj)
    read_num, created = ReadNum.objects.get_or_create(content_type=content_type, object_id=obj.pk)
    return read_num.read_num
