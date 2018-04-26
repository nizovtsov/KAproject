from django.http import HttpResponse
from django.shortcuts import render


from .forms import ContactForm


def home_page(request):
	contact_form = ContactForm()
	context = {
		"title":"Hello world",
		"form": contact_form
	}
	if request.method == "POST":
		print(request.POST)
		print(request.POST.get('email'))
	return render(request, "home_page.html", context)

def about_page(request):
	return render(request, "home_page.html", {})

def contact_page(request):
	return render(request, "home_page.html", {})