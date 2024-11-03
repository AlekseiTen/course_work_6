from django.forms import BooleanField, ModelForm

from mailing.models import Client, Message, Mailing


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class ClientForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Client
        exclude = ("owner",)


class MessageForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Message
        exclude = ("owner",)


class MailingForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Mailing
        exclude = ("owner",)


class MailingManagerForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Mailing
        fields = ("status",)
