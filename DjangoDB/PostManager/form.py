from django import forms

from PostManager.models import Post
from PostManager.validators import validateUserId

class PostForm(forms.Form):
    userId = forms.IntegerField(required=True, label='User id')
    title = forms.CharField(required=True, min_length=1, widget=forms.TextInput)
    body = forms.CharField(required=True, min_length=1, widget=forms.Textarea)

    class Meta:
        model = Post
        fields = ['__all__']


    def clean(self):
        super(PostForm, self).clean()

        if(not validateUserId(self.cleaned_data.get('userId'))):
            self._errors['userId'] = self.error_class(['Invalid user id'])

        if(not len(self.cleaned_data.get('title'))):
            self._errors['title'] = self.error_class(['Length of title must be greater than 0'])

        if (not len(self.cleaned_data.get('body'))):
            self._errors['body'] = self.error_class(['Lenght of body must be greater than 0'])
        return self.cleaned_data
