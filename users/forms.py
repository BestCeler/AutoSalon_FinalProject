from django.contrib.auth.forms import UserCreationForm
from django.db.transaction import atomic
from django.forms import CharField, PasswordInput


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
        widget=PasswordInput(attrs={"placeholder": "Password"})
    )

    password2 = CharField(
        label="Confirm Password",
        widget=PasswordInput(attrs={"placeholder": "Confirm Password"})
    )

    @atomic
    def save(self, commit=True):
        self.instance.is_active = True
        user = super().save(commit) # creates a user
