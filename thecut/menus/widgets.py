from django.forms import FileInput
from django.utils.html import escape
from django.utils.safestring import mark_safe


class ImageInput(FileInput):
    def render(self, name, value, attrs=None):
        output = []
        if value and hasattr(value, 'url'):
            output.append('<a target="_blank" href="%s"><img src="%s" ' \
                'style="display: block; float: left; max-width: 30px;' \
                ' height: 27px; padding-right: 5px;" /></a>' %(
                escape(value.url), escape(value.url)))
        output.append(super(ImageInput, self).render(name, value, attrs))
        return mark_safe(u''.join(output))

