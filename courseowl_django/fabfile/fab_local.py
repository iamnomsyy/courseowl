from django.utils.encoding import force_unicode
from django.utils.text import slugify
from fabric.operations import prompt, local


def branch():
    """
    A simple method to create a branch in "ID-description" style.
    """
    issue_id = slugify(force_unicode(prompt('Issue ID:')))
    short_description = slugify(force_unicode(prompt('Short Description:')))

    if not issue_id or not short_description:
        raise ValueError('[Issue ID] and [Short Description] are'
                         'necessary.')

    issue_id = '{0}'.format(issue_id)

    branch_name = "{0}-{1}".format(issue_id, short_description)
    ru_sure = prompt(
        text='Branch name will be "{0}", Are sure? (y/n)'.format(branch_name),
        default='y'
    )

    if ru_sure != 'y':
        return

    local('git checkout -b "{0}"'.format(branch_name))


def remove_pyc():
    """
    Remove .pyc files in the project directory.
    """
    local('find . -name "*.pyc" -exec rm -f "{}" \;')


def generate_html_docs():
    """
    Generate epydoc HTML documentation.
    """
    local('epydoc --html --parse-only --docformat plaintext accounts api courseowl_django courses website')
