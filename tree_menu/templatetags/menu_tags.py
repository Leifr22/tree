from django import template
from django.urls import resolve, Resolver404
from ..models import MenuItem

register = template.Library()

@register.inclusion_tag('tree_menu/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_path = request.path
    # Попробуем получить имя текущего view
    try:
        current_name = resolve(current_path).view_name
    except Resolver404:
        current_name = None

    # Один запрос: все пункты меню
    qs = MenuItem.objects.filter(menu=menu_name).select_related('parent')

    # Подготовим словарь узлов
    nodes = {}
    for item in qs:
        nodes[item.id] = {
            'item': item,
            'children': [],
            'open': False,
            'active': False,
        }

    # Построим дерево родитель–дочерние
    for node in nodes.values():
        pid = node['item'].parent_id
        if pid and pid in nodes:
            nodes[pid]['children'].append(node)

   
    def mark_active(node):
        itm = node['item']
        is_active = False
        # сравниваем named_url и path
        if itm.named_url and itm.named_url == current_name:
            is_active = True
        elif itm.get_url() == current_path:
            is_active = True

        
        if is_active:
            node['active'] = True
            node['open'] = True
            return True

        
        for child in node['children']:
            if mark_active(child):
                node['open'] = True
                return True
        return False

    
    tree = []
    for node in nodes.values():
        if node['item'].parent_id is None:
            tree.append(node)
            mark_active(node)

    return {'tree': tree}