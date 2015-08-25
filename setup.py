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
    install_requires=['django-mptt>=0.7.2,<0.8',
                      'djangorestframework>=3.1.1,<4', 'pillow>=2.8.1,<3']
)
