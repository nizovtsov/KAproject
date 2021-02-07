from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
import requests
import json
import urllib

from django.conf import settings
from django.core.mail import send_mail

from .forms import ContactForm


def home_page(request):
    #print(request.session.get("first_name", "unknown"))  # get
    context = {
        "title": "Hello world!",
        "content": "Welcome to the home page."
    }
    if request.user.is_authenticated():
        context["premium_content"] = "YEAHHHHHH"
    return render(request, "home_page.html", context)


def about_page(request):
    context = {
        "title": "About Page",
        "content": "Welcome to the about page."
    }
    return render(request, "home_page.html", context)

def listToString(s):
    # initialize an empty string
    str1 = ' '.join(s)

    # return string
    return (str1)

def contact_page(request):
    secret_key = settings.RECAPTCHA_SECRET_KEY
    contact_form = ContactForm(request.POST or None)
    context = {
        "title": "Contact Page",
        "content": "Welcome to the contact page.",
        "form": contact_form,
        'site_key': settings.RECAPTCHA_SITE_KEY
    }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)

    if request.method == "POST":
        ''' Begin reCAPTCHA validation '''
        recaptcha_response = request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req = urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        ''' End reCAPTCHA validation '''

        if result['success']:
            #print(request.POST)
            sub = request.POST
            subject = 'Welcome to DataFlair'
            message = json.dumps(sub)
            recepient = str('Email')
            send_mail('Запрос. Сайт Ком-Авто', message, 'contact@kom-avto.ru', ['wren.systems@gmail.com'], fail_silently=False)
            #send_mail(subject,
             #         message, 'contact@kom-avto.ru', 'contact@kom-avto.ru', fail_silently=False)

            print("ok")


        else:
            print("shit")


        #if not result_json.get('success'):
           # print('robot')
          #  return render(request, 'home_page.html', {'is_robot': True})
        # end captcha verification
        # print(request.POST.get('fullname'))
        # print(request.POST.get('email'))
        #   print(request.POST.get('content'))
    return render(request, "contact/view.html", context)

def home_page_old(request):
    html_ = """
        <!doctype html>
    <html lang="en">
      <head>
        <!-- Required meta tags -->
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

        <!-- Bootstrap CSS -->
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">

        <title>Hello, world!</title>
      </head>
      <body>
      <div class='text-center'>
        <h1>Hello, world!</h1>
      </div>
        <!-- Optional JavaScript -->
        <!-- jQuery first, then Popper.js, then Bootstrap JS -->
        <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>
      </body>
    </html>"""
    return HttpResponse(html_)
