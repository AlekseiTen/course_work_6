from django.forms import ModelForm

from blog.models import Blog


class BlogForm(ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'body', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name,  fild in self.fields.items():
            fild.widget.attrs['class'] = 'form-control'