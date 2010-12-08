from datetime import datetime
from django.contrib.auth.decorators import permission_required, user_passes_test
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.views.decorators.cache import cache_control, cache_page
from thecut.menus.forms import MenuItemAdminForm, MenuMenuItemAdminForm
from thecut.menus.models import Menu, MenuItem
from thecut.menus.settings import SELECTABLE_MODELS
import uuid


@permission_required('menus.add_menu')
def menu_admin_add_child(request, menu_pk):
    """Add/create new child menu."""
    parent_menu = get_object_or_404(Menu, pk=menu_pk)
    if request.is_ajax():
        name = 'New sub menu'
        slug = str(uuid.uuid4())
        menu = Menu(name=slug, slug=slug, publish_at=datetime.now(),
            created_by=request.user, updated_by=request.user)
        menu.save()
        content_type = ContentType.objects.get_for_model(Menu)
        order = parent_menu.menuitem_set.count() + 1
        menu_item = MenuItem(menu=parent_menu, is_enabled=False,
            content_type=content_type, object_id=menu.pk,
            name=name, order=order, publish_at=datetime.now(),
            created_by=request.user, updated_by=request.user)
        menu_item.save()
        return HttpResponse('created', mimetype='text/plain')
    else:
        return HttpResponseBadRequest('bad request')


@cache_control(no_cache=True)
@cache_page(0)
@user_passes_test(lambda u: u.has_perm('menus.add_menuitem') or \
    u.has_perm('menus.change_menuitem'))
def menuitem_admin_contenttype_list(request):
    """Add/create new child menu."""
    if request.is_ajax():
        content_types = []
        for app_model in SELECTABLE_MODELS:
            app_label, model = app_model.lower().split('.')
            content_type = ContentType.objects.get(
                app_label=app_label, model=model)
            content_types += [{'pk': content_type.pk,
                'name': content_type.name.title()}]
        return HttpResponse(simplejson.dumps(content_types),
            mimetype='application/json')
    else:
        return HttpResponseBadRequest('bad request')


@cache_control(no_cache=True)
@cache_page(0)
@user_passes_test(lambda u: u.has_perm('menus.add_menuitem') or \
    u.has_perm('menus.change_menuitem'))
def menuitem_admin_contenttype_object_list(request, content_type_pk):
    """Add/create new child menu."""
    if request.is_ajax():
        content_type = get_object_or_404(ContentType,
            pk=content_type_pk)
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
            item.updated_by = request.user
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
                menuitem.order = menu.menuitem_set.count() + 1
                menuitem.publish_at = datetime.now(),
                menuitem.created_by = request.user
                menuitem.updated_by = request.user
                menuitem.save()
                return HttpResponse('created', mimetype='text/plain')
        else:
            form = MenuItemAdminForm()
        return render_to_response('admin/menus/_menuitem_form.html',
            {'form': form}, context_instance=RequestContext(request))
    else:
        return HttpResponseBadRequest('bad request',
            mimetype='text/plain')


@permission_required('menus.add_menuitem')
def menuitem_admin_add_placeholder(request, menu_pk):
    """Add/create new unlinked (empty) menu item."""
    menu = get_object_or_404(Menu, pk=menu_pk)
    if request.is_ajax():
        name = 'New menu item'
        content_type = ContentType.objects.get_for_model(Menu)
        order = menu.menuitem_set.count() + 1
        menu_item = MenuItem(menu=menu, is_enabled=False,
            content_type=None, object_id=None,
            name=name, order=order, publish_at=datetime.now(),
            created_by=request.user, updated_by=request.user)
        menu_item.save()
        return HttpResponse('created', mimetype='text/plain')
    else:
        return HttpResponseBadRequest('bad request')


@permission_required('menus.change_menuitem')
def menuitem_admin_edit(request, menu_pk, menuitem_pk):
    """Edit/update new menu item."""
    menuitem = get_object_or_404(MenuItem, menu__pk=menu_pk,
        pk=menuitem_pk)
    form_class = menuitem.is_menu and MenuMenuItemAdminForm \
        or MenuItemAdminForm
    print form_class
    if request.is_ajax():
        if request.method == 'POST':
            if menuitem.is_menu:
                form = form_class(request.POST,
                    instance=menuitem)
            else:
                form = form_class(request.POST,
                    instance=menuitem)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.updated_by = request.user
                obj.save()
                return HttpResponse('updated', mimetype='text/plain')
        else:
            form = form_class(instance=menuitem)
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
        data = {'pk': menuitem.pk}
        menuitem.delete()
        return HttpResponse(simplejson.dumps(data),
            mimetype='application/json')
    else:
        return HttpResponseBadRequest('bad request',
            mimetype='text/plain')

