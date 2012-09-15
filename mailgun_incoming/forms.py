# -*- coding: utf-8 -*-
from django import forms

class EmailForm(forms.ModelForm):
    
    field_map = {'from_str':'from',
                 'body_plain':'body-plain',
                 'body_html':'body-html',
                 'stripped_text':'stripped-text',
                 'stripped_html':'stripped-html',
                 'message_headers':'message-headers',
                 'stripped_signature':'stripped-signature',
                 'content_id_map':'content-id-map'}
    
    def __init__(self, *args, **kwargs):
        super(EmailForm, self).__init__(*args, **kwargs)
        for (field_name, form_key) in self.field_map.items():
            self.fields[form_key] = self.fields[field_name]
            del self.fields[field_name]
        self.fields['attachment-count'] = forms.IntegerField(required=False)
        
    def clean(self):
        for (field_name, form_key) in self.field_map.items():
            if form_key in self.cleaned_data:
                self.cleaned_data[field_name] = self.cleaned_data[form_key]
        return self.cleaned_data