from django.contrib.auth.forms import UserCreationForm
from django.forms import CharField


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ["username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2"]
        labels = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "E-mail",
        }

    password1 = CharField(
        label="Password",
    )