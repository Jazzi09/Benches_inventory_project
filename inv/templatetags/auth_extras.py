
from django import template

register = template.Library()

@register.filter
def in_group(user, group_name: str) -> bool:
    # Returns True if user belongs to the group
    try:
        return user.is_authenticated and user.groups.filter(name=group_name).exists()
    except Exception:
        return False
