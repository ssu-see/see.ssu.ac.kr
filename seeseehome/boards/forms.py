"""
from django import forms
from ckeditor.fields import RichTextFormField
from ckeditor.widgets import CKEditorWidget

class WriteForm(forms.Form):
#   content = RichTextFormField()

#   For more Custom Client API, subject form was implemented
#   in template(html)

#   This form is not used. It is just for reference
    content = forms.CharField(
                  label="",
                  widget=CKEditorWidget(),
                  max_length = 65535,
              )
"""

from django import forms
from boards.models import Board
from seeseehome import msg
from django.core.exceptions import ValidationError


class BoardForm(forms.ModelForm):

    def clean_boardname(self):
        #       More than Max number of boards?
        try:
            Board.objects.validate_max_number_of_boards(
                Board.objects.all().count()
            )
        except ValidationError:
            raise forms.ValidationError(msg.boards_max_number_of_boards)

#       Board name validator
        try:
            Board.objects.validate_boardname(self.cleaned_data["boardname"])
        except ValueError:
            raise forms.ValidationError(msg.boards_name_must_be_set)
        except ValidationError:
            raise forms.ValidationError(msg.boards_name_at_most_30)

        return self.cleaned_data["boardname"]
