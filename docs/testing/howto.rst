==================
Running unit tests
==================


Using a virtualenv
------------------

You can use ``virtualenv`` to test without polluting your system's Python environment.
The only way to test correctly is in the virtualenv. We use Python 2 and Django 1.8
as the default test env. Tox then tests the alternative configs

1. Install ``virtualenv``::

    $ pip install virtualenv

2. Create and activate a ``virtualenv``::

    $ cd thecut-menus
    $ virtualenv .
    $ source bin/activate
    (thecut-menus) $

3. Manually link to thecut requirements.
    In python 3 we have issues with package namespaces being shared between site-packages
    and the local directory. So we need to link manually. You will need to manually clone
    the following package and checkout master
    thecut-authorship
    thecut-ordering
    thecut-publishing
    (thecut-menus) $ cd thecut
    (thecut-menus) $ ln -s ~/thecut-authorship/thecut/authorship .
    (thecut-menus) $ ln -s ~/thecut-ordering/thecut/ordering .
    (thecut-menus) $ ln -s ~/thecut-publishing/thecut/publishing .
    (thecut-menus) $ cd ..


4. Install the test suite requirements::

    (thecut-menus) $ pip install -r requirements-test.txt

5. Ensure a version of Django is installed::

    (thecut-menus) $ pip install "Django>=1.8,<1.9"

6. Run the test runner::

    (thecut-menus) $ python runtests.py


Using tox
---------------------------------

You can use tox to automatically test the application on a number of different
Python and Django versions.

1. Install ``tox``::

    $ pip install -r requirements-test.txt

2. Run ``tox``::

    (thecut-menus) $ tox --recreate

Tox assumes that a number of different Python versions are available on your
system. If you do not have all required versions of Python installed on your
system, running the tests will fail. See ``tox.ini`` for a list of Python
versions that are used during testing.

Test coverage
-------------

The included ``tox`` configuration automatically detects test code coverage with ``coverage``::

      $ coverage report -m
