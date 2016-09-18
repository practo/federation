from fabric.api import lcd, task, settings, hide
from fabpolish import polish, sniff, local, info
from fabpolish.contrib import find_merge_conflict_leftovers
import os
from subprocess import call

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

# @sniff(severity='major', timing='fast')
# def run_eslint():
#     info('Running ESLint...')
#     return local(
#         "git ls-files | "
#         "grep '\.js$' | "
#         "xargs ./node_modules/eslint/bin/eslint.js  --config=.eslintrc"
#     )

@sniff(severity='major', timing='fast')
def remove_compiled_classes():
    info('Removing compiled python classes...')
    local('pyclean .')
    return local(
        'find ./app -name "*.py[co]" -print0 | xargs -0 rm -f'
    )


@sniff(severity='major', timing='fast')
def fix_directory_permission():
    info('Fixing directory permissions...')
    return local(
        '! find ./app '
        '-path .git -prune -o '
        '-name .webassets-cache -prune -o '
        '-name gen -prune -o '
        '-type d -not -perm 0775 -print0 | '
        'tee /dev/stderr | '
        'xargs -0 chmod 0775 >/dev/null 2>&1'
    )


@sniff(severity='major', timing='fast')
def fix_file_permission():
    """Fixing permissions for files"""
    info('Fixing permissions for files...')
    return local(
        "git ls-files -z | "
        "grep -PvZz '\.sh$' | "
        "grep -PvZz 'tests/' | "
        "xargs -0 chmod -c 0664 > /dev/null 2>&1"
    )


@sniff(severity='major', timing='fast')
def check_code_standard():
    """Running coding standards check"""
    info('Running coding standards check...')
    return local(
        'pep8 ./app'
    )


@sniff(severity='major', timing='fast')
def static_code_analyzer():
    """Running static code analyzer"""
    info('Running static code analyzer...')
    return local(
        'pyflakes ./app'
    )


@sniff(severity='major', timing='fast')
def check_print_statement():
    """Checking for debug print statements"""
    info('Checking for debug print statements...')
    return local(
        '! find ./app -type f -name "*.py" -print0 | '
        'xargs -0 grep -Pn \'(?<![Bb]lue|>>> )print\' | '
        'grep -v NOCHECK'
    )


@sniff(severity='major', timing='fast')
def servername_compatibility():
    """Checking for no-servername compatibility"""
    info('Checking for no-servername compatibility...')
    return local(
        '! find ./app -name "default_settings.py" -o '
        ' -type f -name "*.py" -print0 | '
        'xargs -0 grep -Pn \'SERVER_NAME|ENABLE_HTTPS|SSO_DOMAIN|'
        '(SOFTWARE(_WEBSITE)?|EPICENTER|FABRIC|PVR|PRACTONAV)_HOST\''
    )


# @sniff(severity='major', timing='fast')
# def check_migrations():
#     """Checking migration branches"""
#     info('Checking migration branches...')
#     return local(
#         '! alembic branches | grep branchpoint'
#     )


# @sniff(severity='major', timing='fast')
# def run_tests():
#     """Running tests"""
#     info('Running tests...')
#     value = 'PYTHONPATH="%s" FLASK_ENV=TEST python ./tests/run_tests.py' % ROOT_DIR
#     return local(
#         value
#     )


@task
def grep(term, flags=''):
    with lcd(ROOT_DIR), settings(hide('running')):
        local('find app tests '
              '-name "*~" -o '
              '-name "*.py[co]" -o '
              '-name "*.dot" -o '
              '-name "*.min.*" -o '
              '-name "gen" -prune -o '
              '-name ".webassets-cache" -prune -o '
              '-type d -o '
              '-print0 | '
              'xargs -0 grep -n --color=force ' + flags + ' "' + term + '"; '
              ' echo -n')
