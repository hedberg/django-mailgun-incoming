from distutils.core import setup

setup(
    name='django-mailgun-incoming',
    version='0.1dev',
    author='Simon Hedberg',
    author_email='simon@in-formation.se',
    packages=['mailgun_incoming'],
    url='http://github.com/hedberg/django-mailgun-incoming/',
    description='Django app for storing email and attached files received through the Mailgun API.',
    long_description=open('README.rst').read(),
    install_requires=[
        "Django >= 1.3",
    ],
)