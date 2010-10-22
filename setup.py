from distutils.core import setup


setup(name='menus',
    author='Busara', author_email='serveradmin@busara.com.au',
    url="http://projects.busara.com.au/projects/django-app-menus",
    version='0.01',
    packages=['menus', 'menus.templatetags'],
    package_data={
        'menus': ['templates/menus/*.*',
            'templates/admin/menus/*.*',
            'templates/admin/menus/edit_inline/*.*',
            'media/menus/javascripts/*.*', 'media/menus/stylesheets/*.*',
            'media/menus/images/*.*',
            ]},
    requires=['thecut'],
    )

