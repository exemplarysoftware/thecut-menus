from datetime import datetime
from django.contrib.auth.decorators import permission_required, user_passes_test
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils import simplejson
from menus.forms import MenuItemAdminForm
from menus.models import Menu, MenuItem
import uuid


@permission_required('menus.add_menu')
def menu_admin_add_child(request, menu_pk):
    """Add/create new child menu."""
    parent_menu = get_object_or_404(Menu, pk=menu_pk)
    if request.is_ajax():
        name = str(uuid.uuid4())
        menu = Menu(name=name, slug=name, publish_at=datetime.now())
        menu.save()
        content_type = ContentType.objects.get_for_model(Menu)
        menu_item = MenuItem(menu=parent_menu, content_type=content_type,
            object_id=menu.pk, order=100, publish_at=datetime.now())
        menu_item.save()
        return HttpResponse('created', mimetype='text/plain')
    else:
        return HttpResponseBadRequest('bad request')


@user_passes_test(lambda u: u.has_perm('menus.add_menuitem') or \
    u.has_perm('menus.change_menuitem'))
def menuitem_admin_contenttype_list(request, content_type_pk):
    if request.is_ajax():
        content_type = get_object_or_404(ContentType, pk=content_type_pk)
        model_class = content_type.model_class()
        
        objects = []
        for obj in model_class.objects.all():
            objects += [{'pk': obj.pk, 'name': str(obj)}]
        
        return HttpResponse(simplejson.dumps(objects),
            mimetype='application/json')
    else:
        return HttpResponseBadRequest('bad request')


@permission_required('menus.change_menuitem')
def menuitem_admin_reorder(request):
    """Reorder list of menu items."""
    if request.is_ajax() and request.method == 'POST':
        order = request.REQUEST.get('order').split(',')
        for pk in order:
            item = MenuItem.objects.get(pk=pk)
            item.order = order.index(pk)
            item.save()
        return HttpResponse('ok', mimetype='text/plain')
    else:
        return HttpResponseBadRequest('bad request',
            mimetype='text/plain')


@permission_required('menus.add_menuitem')
def menuitem_admin_add(request, menu_pk):
    """Add/create new menu item."""
    menu = get_object_or_404(Menu, pk=menu_pk)
    if request.is_ajax():
        if request.method == 'POST':
            form = MenuItemAdminForm(request.POST)
            if form.is_valid():
                menuitem = form.save(commit=False)
                menuitem.menu = menu
                menuitem.publish_at = datetime.now()
                menuitem.save()
                return HttpResponse('created', mimetype='text/plain')
        else:
            form = MenuItemAdminForm()
        return render_to_response('admin/menus/_menuitem_form.html',
            {'form': form}, context_instance=RequestContext(request))
    else:
        return HttpResponseBadRequest('bad request',
            mimetype='text/plain')


@permission_required('menus.change_menuitem')
def menuitem_admin_edit(request, menu_pk, menuitem_pk):
    """Edit/update new menu item."""
    menuitem = get_object_or_404(MenuItem, menu__pk=menu_pk,
        pk=menuitem_pk)
    if True:#request.is_ajax():
        if request.method == 'POST':
            form = MenuItemAdminForm(request.POST, instance=menuitem)
            if form.is_valid():
                form.save()
                return HttpResponse('updated', mimetype='text/plain')
        else:
            form = MenuItemAdminForm(instance=menuitem)
        return render_to_response('admin/menus/_menuitem_form.html',
            {'form': form, 'menuitem': menuitem},
            context_instance=RequestContext(request))
    else:
        return HttpResponseBadRequest('bad request',
            mimetype='text/plain')


@permission_required('menus.delete_menuitem')
def menuitem_admin_delete(request, menu_pk, menuitem_pk):
    """Delete/destroy existing menu item."""
    menuitem = get_object_or_404(MenuItem, menu__pk=menu_pk,
        pk=menuitem_pk)
    if request.is_ajax() and request.method == 'POST':
        menuitem.delete()
        return HttpResponse('deleted', mimetype='text/plain')
    else:
        return HttpResponseBadRequest('bad request',
            mimetype='text/plain')

