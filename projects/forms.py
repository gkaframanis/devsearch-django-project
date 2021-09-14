from django.forms import ModelForm
from django import forms
from .models import Project


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ["title", "featured_image", "description", "demo_link", "source_link", "tags"]
        # 1st way to customize the form fields
        widgets = {"tags": forms.CheckboxSelectMultiple()}

    # 2nd way overwriting the __init__ method
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        # self.fields["title"].widget.attrs.update({"class": "input"})
        # Loop a dictionary (key, value in items())
        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})
