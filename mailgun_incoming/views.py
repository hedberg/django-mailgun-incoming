# -*- coding: utf-8 -*-
import hashlib, hmac
import logging
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.forms.models import modelform_factory
from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from mailgun_incoming.models import Attachment, IncomingEmail
from mailgun_incoming.signals import email_received
from mailgun_incoming.forms import EmailForm

logger = logging.getLogger(__name__)

API_KEY = getattr(settings, "MAILGUN_ACCESS_KEY", "")
VERIFY_SIGNATURE = getattr(settings, "MAILGUN_VERIFY_INCOMING", API_KEY!="")

class Incoming(View):
    email_model = IncomingEmail
    attachment_model = Attachment
    form = EmailForm
    api_key = API_KEY
    verify = VERIFY_SIGNATURE
    
    def get_form(self):
        return modelform_factory(self.email_model, form=self.form)
    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(Incoming, self).dispatch(*args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        if self.verify:
            verified = self.verify_signature(request.POST.get('token',''),
                              request.POST.get('timestamp',''),
                              request.POST.get('signature',''))
            if not verified:
                logger.debug("Signature verification failed. Email posted from %s. %s" % (
                              request.META.get('REMOTE_ADDR','<no remote addr>'),
                              request.POST.get('subject', '')))
                return HttpResponseBadRequest("Invalid signature")
                
        form = self.get_form()(request.POST)
        
        if form.is_valid():
            #save email
            email = form.save()
            #save attachments
            attachments = []
            if form.cleaned_data.get('attachment-count',0):
                attachments = []
                #reverse mapping in content_ids dict
                content_ids = dict((attnr,cid) for cid,attnr in (email.content_ids or {}).iteritems())
                i = 1
                for file in request.FILES.values():
                    attachment = self.attachment_model(email=email, file=file, content_id=content_ids.get('attachment-{0!s}'.format(i),'')).save()
                    attachments.append(attachment)
                    i += 1
            self.handle_email(email, attachments=attachments)
        else:
            logger.debug("Received email message contained errors. %s" % form.errors)
        
        return HttpResponse("OK")
    
    def handle_email(self, email, attachments=None):
        email_received.send(sender=self.email_model, instance=email, attachments=attachments or [])
    
    def verify_signature(self, token, timestamp, signature):
        return signature == hmac.new(key=self.api_key,
                                 msg='{0}{1}'.format(timestamp, token),
                                 digestmod=hashlib.sha256).hexdigest()
