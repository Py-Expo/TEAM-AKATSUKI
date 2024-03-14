from django.shortcuts import render
from django.http import HttpResponse
from .models import *
import yagmail
import os


def home(request):
    return render(request,'index.html')
def detect(request):
    return render(request, 'detect.html')
def contact(request):
    return render(request, 'contact.html')

def getintouch(request):
    if request.method=="POST":
        name = request.POST.get('Name')
        phone = request.POST.get('Phone number')
        email = request.POST.get('Email')
        message = request.POST.get('Message')

        Touch.objects.create(
        name=name,
        phone=phone,
        email=email,
        message=message)


        mail(name,email, message)

        return render(request, 'index.html')
    
    return HttpResponse("Invalid request method or no data provided.")
    
def mail(name, email, message):
    subject = 'Inquiry for Get-in-Touch Form'
    company = "Lane Detection"
    your_name = "Roshan"
    your_title = "CEO"
    contact_information = "hahahaharitwo@gmail.com"

    # Format the email body
    body = f"""
    Hi {name},
    I hope this message finds you well. We received an inquiry via our Get-in-Touch form.
    Details:
    Name: {name}
    Email: {email}
    Message: {message}




    {your_name}
    {your_title}
    {company}
    {contact_information}
    """
    
    gmail_username = 'hahahaharitwo@gmail.com'
    sender_name = 'Hari'

    yag = yagmail.SMTP('hahahaharitwo@gmail.com', 'ajre miny mftv emza')
    

    yag.send(
        to=email,
        subject=subject,
        contents=body,
        headers={'From': f'{sender_name} <{gmail_username}>'},
    )


def news(request):
    if request.method=="POST":
        email = request.POST.get('Email')

        newsletter.objects.create(
        email=email,)

        news_mail(email)

        return render(request, 'index.html')
    
    return HttpResponse("Invalid request method or no data provided.")

def news_mail(email):
    subject = 'Newsletter from LD'
    company = "Lane Detection"
    your_name = "Roshan"
    your_title = "CEO"
    contact_information = "hahahaharitwo@gmail.com"

    gmail_username = 'hahahaharitwo@gmail.com'
    sender_name = 'Hari'

    yag = yagmail.SMTP('hahahaharitwo@gmail.com', 'ajre miny mftv emza')
    
    file_path = r"D:\Pyexpo\dj_project\media\Newsletter.docx"


    # Format the email body
    body = f"""
    Hi,
    I hope this message finds you well. We send our monthly newsletter below.

    {your_name}
    {your_title}
    {company}
    {contact_information}
    """

    yag.send(
        to=email,
        subject=subject,
        contents=body,
        headers={'From': f'{sender_name} <{gmail_username}>'},
        attachments=[file_path],
    )


