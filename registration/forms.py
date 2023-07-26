from django import forms
from blog.models import Author

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ('first_name', 'last_name', 'date_of_birth')