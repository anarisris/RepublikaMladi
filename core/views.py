# coding=utf-8
from django.shortcuts import render_to_response, render
from republika.core.models import *
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template.context import RequestContext
from django.shortcuts import get_object_or_404
import datetime
from republika.core.forms import *
from django.conf import settings


def contact(request):
    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) # A form bound to the POST data
        if form.is_valid():
	    subject = form.cleaned_data['subject']
	    message = form.cleaned_data['message']
	    sender = form.cleaned_data['sender']
	    cc_myself = form.cleaned_data['cc_myself']

	    recipients = ['tamara@reactor.org.mk']
	    if cc_myself:
		recipients.append(sender)

	    from django.core.mail import send_mail
	    send_mail(subject, message, sender, recipients)
	    return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = ContactForm() # An unbound form

    return render(request, 'contact.html', {
        'form': form,
    })

def contactDebate(request):
    if request.method == 'POST': # If the form has been submitted...
        form = ContactFormDebate(request.POST) # A form bound to the POST data
        if form.is_valid():
	    subject = form.cleaned_data['subject']
	    debate_title = form.cleaned_data['debate_title']
            debate_scope = form.cleaned_data['debate_scope']
            debate_description = form.cleaned_data['debate_description']
	    sender = form.cleaned_data['sender']
	    cc_myself = form.cleaned_data['cc_myself']

	    recipients = ['tamara@reactor.org.mk']
	    if cc_myself:
		recipients.append(sender)

	    from django.core.mail import send_mail
            message = debate_title
	    send_mail(subject, message, sender, recipients)
	    return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = ContactFormDebate() # An unbound form

    return render(request, 'newdebate.html', {
        'form': form,
    })

def contactDocument(request):
    if request.method == 'POST': 
        form = ContactFormDocument(request.POST, request.FILES) 
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            attach = request.FILES.get('attach')

	    from django.core.mail import EmailMessage
            mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [sender])
            if attach is not None:
                mail.attach(attach.name, attach.read(), attach.content_type)
            mail.send()
	    return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = ContactFormDocument() # An unbound form

    return render(request, 'newdocument.html', {
        'form': form,
    })
            

