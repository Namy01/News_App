from django import forms
from newspaper.models import Post, Tag, Category
from django_summernote.widgets import SummernoteWidget

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ("author","views_count", "published_at")
        widgets = {
            "title" : forms.TextInput(
                attrs= 
                {
                    "class" : "form-control",
                    "placeholder" : "Enter the title of the post",
                }
            ),
            "content" : SummernoteWidget(
                attrs = {
                    "summernote": {
                        "width": "100%",
                        "height" : "400px",
                    },
                }
            ),
            "status": forms.Select(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "tag": forms.SelectMultiple(attrs={"class": "form-control"}),

        }
       

        

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ("name",)
        widgets = {
            "name" : forms.TextInput(
                attrs= 
                {
                    "class" : "form-control",
                    "placeholder" : "Enter the name of the tag",
                }
            )
         }



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name",)
        widgets = {
            "name" : forms.TextInput(
                attrs= 
                {
                    "class" : "form-control",
                    "placeholder" : "Enter the name of the category",
                }
            )
         }
