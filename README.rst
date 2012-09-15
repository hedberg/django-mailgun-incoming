=======================
Django-Mailgun-Incoming
=======================
:Info: A Django app for receival and storage of incoming emails from Mailgun
:Author: Simon Hedberg (http://github.com/hedberg, http://twitter.com/SimonHedberg)

This README is derived from https://github.com/hmarr/django-ses/blob/master/README.rst

Overview
=================
Django-Mailgun-Incoming stores email and attached files received through the Mailgun_ API.
The goal of this package is to be easy to use and easy to customise when needed.

.. _Mailgun: http://mailgun.net

Getting started
=================


Requirements
------------

- Django 1.3 or higher (class based views).

Installation
------------

- Install the package by cloning the repository to your Python path or install using pip::

    pip install git+https://github.com/hedberg/django-mailgun-incoming.git#egg=mailgun_incoming

- Add ``"mailgun_incoming"`` to your ``INSTALLED_APPS`` setting::

    INSTALLED_APPS = [
        # ...
        "mailgun_incoming",
    ]

- Include urls. 
    
    url('^email/', include('mailgun_incoming.urls')),
    
    Point your Mailgun forwarding to the URL used, i.e. /email/incoming/ using the above URL configuration.

- Settings

    MAILGUN_ACCESS_KEY (optional)
    - This is used to verify the signature in posted data. 
    
    MAILGUN_VERIFY_SIGNATURE (optional)
    - This defaults to True if MAILGUN_ACCESS_KEY is specified. Can be set to False for debugging etc.
    
    MAILGUN_UPLOAD_TO (optional)
    - This can be used to specify where attachments should be saved. This is passed to the file field. Defaults to 'attachments/'

Basic Usage
-----------
    
    Using the default settings incoming emails are stored in the database and triggers the ``mailgun_incoming.signals.email_received`` signal for further processing.

    Three models are included in the package. EmailBaseModel - an abstract base model, IncomingEmail - which extends the base model adding a user field and Attachment - a basic model for storing incoming file attachments.

    Processing of incoming data are done in the Incoming view which is class based.

Customisation
-------------

    Customisation can be done by

    - adding processing logic triggered by the email_recieved signal
    - extending the email model
    - passing parameters to the Incoming view
    - subclassing the Incoming view
