from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "password1", "password2"]
        labels = {
            "first_name": "First Name",
            "last_name": "Last Name"
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        # self.fields["title"].widget.attrs.update({"class": "input"})
        # Loop a dictionary (key, value in items())
        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})
