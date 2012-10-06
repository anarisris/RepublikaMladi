from django import forms

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)


class ContactFormDebate(forms.Form):

    subject = forms.CharField(max_length=100)
    debate_title = forms.CharField(max_length=100)
    debate_description = forms.CharField()
    debate_scope = forms.CharField(max_length=200)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)


class ContactFormDocument(forms.Form):

    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    attach = forms.Field(required=False, widget = forms.FileInput)
    sender = forms.EmailField()
    
