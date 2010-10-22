from django.contrib.auth.decorators import user_passes_test
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import simplejson


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

