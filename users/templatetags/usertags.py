from django import template

register = template.Library()

@register.filter()
def has_group(user, group_name):
    groups = user.preferch_related('groups').groups.all().values_list('name', flat=True)
    return True if group_name in groups else False