from django import forms
from .models import Shop_Post, Size, Comment


class ShopPostForm(forms.ModelForm):
    """name=forms.CharField(max_length=80)
    body=forms.Textarea()
    size=forms.ChoiceField(choices=[size for size in Size.objects.all()])"""

    class Meta:
        model=Shop_Post
        fields=['title', 'body',"size", "status"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "email", "body"]
        # exclude=[...] 
