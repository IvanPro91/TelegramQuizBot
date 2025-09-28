from django import forms

from quiz.models import TelegramQuiz


class TelegramQuizFromCreate(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TelegramQuizFromCreate, self).__init__(*args, **kwargs)
        self.fields["quest"].widget.attrs.update({"class": "form-control"})
        self.fields["hint"].widget.attrs.update({"class": "form-control", "rows": "3"})

    class Meta:
        model = TelegramQuiz
        fields = (
            "quest",
            "hint",
        )
