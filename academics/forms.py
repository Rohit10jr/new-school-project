from email.policy import default
from logging import PlaceHolder
from pyexpat import model
from django import forms
from .models import *


class Questionform(forms.ModelForm):
    class Meta:
        model = Question
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(Questionform, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class Answerform(forms.ModelForm):
    class Meta:
        model = Answer
        fields = "__all__"
        exclude = ['question']


class Chapterform(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = "__all__"
        exclude = ['subject']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'allChapter':
                print(type(field_name), field_name)
                field.widget.attrs['class'] = 'form-control'


class Subjectform(forms.ModelForm):
    class Meta:
        model = Subject
        fields = "__all__"
        exclude = ['grade']


class Loginform(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Email"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone"}))


class grade_form(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['grade']


class subject_form(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'


class chapter_form(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = '__all__'


class chapterlist_form(forms.Form):
    grade = forms.CharField(max_length=14)
    subject = forms.CharField(max_length=20)


class subjectlist_form(forms.Form):
    grade = forms.CharField(max_length=14)


class questionlist_form(forms.ModelForm):
    # grade_name = forms.CharField(max_length=14)
    no_of_questions = forms.CharField(max_length=20)

    class Meta:
        model = Question
        fields = ['grade', 'subject', 'chapter', 'no_of_questions',]


class question_form(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'


class form_for_chapterlist(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['grade', ]


class answer_form(forms.ModelForm):
    ans = question_form

    class Meta:
        model = Answer
        fields = '__all__'
        exclude = ['question', ]


class TestForm(forms.ModelForm):
    timing = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={"placeholder": "duration in seconds"}))
    overall_marks = forms.IntegerField(min_value=0)

    class Meta:
        model = Test
        fields = ['timing', 'overall_marks', 'remarks', 'description', 'pass_percentage']
        

class instruction_form(forms.Form):
    instruction = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", 
                    "placeholder": "Instructions", "style": "color:black; width:50%;"}))


class questionCustomForm(forms.Form):
    from_chapter = forms.ChoiceField()
    to_chapter = forms.ChoiceField()
    allChapter = forms.BooleanField()

    def __init__(self, *args, **kwargs):
        super(questionCustomForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'allChapter':
                print(type(field_name), field_name)
                field.widget.attrs['class'] = 'form-control'


class customizeForm(forms.Form):
    Chapter = forms.ChoiceField()
    cognitive_level = forms.ChoiceField()
    no_cognitive_level = forms.IntegerField(label='')
    difficulty_level = forms.ChoiceField()
    no_difficulty_level = forms.IntegerField(label='')