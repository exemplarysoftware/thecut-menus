from __future__ import print_function
from __future__ import absolute_import

from setuptools import setup, find_packages
import io
import os
from thecut.menus import __version__


here = os.path.abspath(os.path.dirname(__file__))


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        filename = os.path.join(here, filename)
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.rst', 'HISTORY.rst')

setup(
    # General information
    name='thecut-menus',
    version=__version__,

    # Packaging
    packages=find_packages(exclude=['docs']),
    namespace_packages=['thecut'],
    include_package_data=True,

    # Dependencies
    install_requires=['django-mptt>=0.8.7',
                      'djangorestframework>=3.6.2,<4', 'pillow>=4.1.1,<5'],

    # Author information
    author='The Cut Creative',
    author_email='development@thecut.net.au',

    # Additional information
    url='https://projects.thecut.net.au/projects/thecut-menus',
    license='Apache Software License 2.0',
    description='A reusable application.',
    long_description=long_description,
    platforms='any',
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
    ],
)


"""
from setuptools import setup, find_packages
from version import get_git_version


setup(
    name='thecut-menus',
    author='The Cut',
    author_email='development@thecut.net.au',
    url='http://projects.thecut.net.au/projects/thecut-menus',
    namespace_packages=['thecut'],
    version=get_git_version(),
    packages=find_packages(),
    include_package_data=True,
    #install_requires=['django-mptt>=0.7.2,<0.8',
    #                  'djangorestframework>=3.1.1,<4', 'pillow>=2.8.1,<3']
    install_requires=[]
)
"""
