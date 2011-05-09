from setuptools import setup, find_packages
from version import get_git_version

setup(name='menus',
    author='The Cut', author_email='development@thecut.net.au',
    url='http://projects.thecut.net.au/projects/django-app-menus',
    namespace_packages=['thecut'],
    version=get_git_version(),
    packages=find_packages(),
    include_package_data=True,
    install_requires=['distribute', 'django-form-utils==0.2.0'],
    )

