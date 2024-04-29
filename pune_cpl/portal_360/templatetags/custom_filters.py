from django import template

register = template.Library()

@register.filter
def get_property_ids(queryset):
    return [item['property_id'] for item in queryset]

@register.filter
def get_property_tax(queryset):
    return [float(item['total_tax']) for item in queryset]

@register.filter(name='get_range')
def get_range(value):
    return range(1, value + 1)