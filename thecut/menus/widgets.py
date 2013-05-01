# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.utils.html import escape
from django.utils.safestring import mark_safe

try:
    from django.forms import ClearableFileInput as FileInput
except ImportError:
    from django.forms import FileInput


class ImageInput(FileInput):

    def render(self, name, value, attrs=None):
        output = []
        if value and hasattr(value, 'url'):
            image_html = '<a target="_blank" href="{url}" class="image">' \
                '<img src="{url}" alt="" /></a>'
            output.append(image_html.format(url=escape(value.url)))
        output.append(super(ImageInput, self).render(name, value, attrs))
        return mark_safe(''.join(output))
