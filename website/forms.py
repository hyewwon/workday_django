from django import forms
from website.models import Notice, FreeBoard
from django_summernote.widgets import SummernoteWidget


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'id' : 'title',
                'class': "form-control",
                "placeholder" : "제목을 입력해주세요."
            }),
            'content': SummernoteWidget(attrs={
                'summernote': {'width': '100%', 'height': '1000px'},
                'placeholder' : "내용을 입력해 주세요."
                }),
        }


class FreeBoardForm(forms.ModelForm):
    class Meta:
        model = FreeBoard
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'id' : 'title',
                'class': "form-control",
                "placeholder" : "제목을 입력해주세요.",
            }),
            'content': SummernoteWidget(attrs={
                'summernote': {'width': '100%', 'height': '1000px'},
                'placeholder' : "내용을 입력해 주세요."
                }),
        }




        

        

