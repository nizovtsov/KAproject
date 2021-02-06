from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class ContactForm(forms.Form):
    fullname = forms.CharField(label='Имя',
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "form_fullname",
                "placeholder": "Ваше имя"
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "id": "form_email",
                "placeholder": "Ваш email"
            }
        ))
    content = forms.CharField(label='Чем мы можем помочь?',
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "id": "form_content",
                "placeholder": "Ваше сообщение"
            }
        )
    )

    def clean_email(self):
        email = self.cleaned_data.get("email") #TODO email validation
        #if not "gmail.com" in email:
        #    raise forms.ValidationError("Email has to be gmail.com")

        return email


