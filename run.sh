#!/bin/bash

export PYTHONPATH=".:$PYTHONPATH"
export DJANGO_SETTINGS_MODULE="test_app.settings"

usage() {
    echo "USAGE: $0 [command]"
    echo " test - run the tests"
    echo " shell - open the Django shell"
    echo " schema - create a schema migration for any model changes"
    exit 1
}

case "$1" in
    "test" )
        django-admin.py test ;;
    "shell" )
        django-admin.py shell ;; # TODO: y u no work?
    "schema" )
        django-admin.py schemamigration menus --auto ;;
    * )
        usage ;;
esac
