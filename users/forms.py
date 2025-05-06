import profile

from django.contrib.auth.forms import UserCreationForm
from django.db.models import IntegerField
from django.db.transaction import atomic
from django.forms import CharField, PasswordInput, IntegerField

from users.models import Profile

# Create a user
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

    phone = IntegerField(
        label='Telephone number',
        required=True
    )


    password1 = CharField(
        label="Password",
        widget=PasswordInput(attrs={"placeholder": "Password"})
    )

    password2 = CharField(
        label="Confirm Password",
        widget=PasswordInput(attrs={"placeholder": "Confirm Password"})
    )

    phone = IntegerField(
        label="Phone Number",
        required=True
    )

    @atomic
    def save(self, commit=True):
        self.instance.is_active = True
        user = super().save(commit) # creates a user
        phone = self.cleaned_data.get("phone")
        profile = Profile(
            user=user,
            phone_num = self.cleaned_data['phone'],
        )
        if commit:
            profile.save() # saves created profile
        return user
