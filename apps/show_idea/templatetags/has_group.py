from django import template

register = template.Library()


# 前端模板加上过滤器
@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
