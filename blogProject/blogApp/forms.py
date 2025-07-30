from django import forms
from blogApp.models import postModel,commentModel

class postForm(forms.ModelForm):
    class Meta():
        model  = postModel
        fields = ('author','title','text')

        widgets = {
                     'title':forms.TextInput(attrs={'class':'textinputclass'}),
                     'text': forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})
                  }

class commentForm(forms.ModelForm):
    class Meta():
        model  = commentModel
        fields = ('author','post','text')

        widgets = {
                     'author':forms.TextInput(attrs={'class':'textinputclass'}),
                     'text': forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})
                  }