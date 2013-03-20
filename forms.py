from django.forms import *
from culinary.models import *


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ["post"]

    def clean_author(self):
        return self.cleaned_data.get("author") or "Anonymous"
