from django.db import models
from datetime import datetime 
from venv import create
from time import timezone
from unittest import result
from django.conf import settings
from django.db import DatabaseError, models 
from django.core.validators import MaxValueValidator, MinValueValidator, MaxLengthValidator
from django.contrib.postgres.fields import ArrayField, HStoreField
import re 
import uuid
import jsonfield
from accounts.models import User
from django.forms import IntegerField
# Create your models here.


'''
1.  check if can use forginkey field instead of that model field turn str(self.field)
A. you can check the subject model return (str(self.subject))+' '+(self.name)
2. please check and understand the custom def save()
3. def.save() doesnt update the values, check that 
'''

class Grade(models.Model):
    grade = models.PositiveIntegerField(null=True, validators=[MaxValueValidator(12)])
    section = ArrayField(models.CharField(max_length=1, blank=True),blank=True, default=list)

    def __str__(self):
        return str(self.grade)
    
    class Meta:
        ordering = ('grade',)


class Subject(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.grade) + ' ' + self.name

    def save(self, *args, **kwargs):
        name = re.findall(r"[^\W\d_]+|\d+", self.name) # Extracts words and digits
        # print(name)
        self.name = (' '.join(name)).upper() # Joins them with spaces and converts to lowercase
        super(Subject, self).save(*args, **kwargs) # Calls the parent save method

    class Meta:
        ordering = ('grade', 'code', 'name',)


class Chapter(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    chapter_no = models.PositiveIntegerField(null=True,validators=[MaxValueValidator(12)])
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (str(self.subject))+' '+(self.name)

    # check
    def save(self, *args, **kwargs):
        # self.created_at = (datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
        name = re.findall(r"[^\W\d_]+|\d+", self.name)
        self.name = (' '.join(name)).lower()
        super(Chapter, self).save(*args, **kwargs)

    class Meta:
        ordering = ('subject', 'chapter_no',)


questiontype_choice = (
    ('MCQ', 'MCQ'),
    ('Fill_in_the_blanks', 'Fill_in_the_blanks'),
    ('Match_the_following', 'Match_the_following')
)

cognitive_level = (
    ('Knowledge', 'Knowledge'),
    ('Comprehension', 'Comprehension'),
    ('Application', 'Application')
)

difficulty_level = (
    ('Easy', 'Easy'),
    ('Medium', 'Medium'),
    ('Hard', 'Hard')
)


class Question(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, null=True)
    question = models.CharField(max_length=50)
    duration = models.PositiveIntegerField(default=30)
    mark = models.PositiveIntegerField(default=1)
    chapter_no = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    cognitive_level = models.CharField(max_length=20, choices=cognitive_level, default=cognitive_level[0][0])
    question_type = models.CharField(max_length=20, choices=questiontype_choice, default=questiontype_choice[0][0])
    difficulty_level = models.CharField(max_length=20, choices=difficulty_level, default=difficulty_level[0][0])

    def __str__(self):
        return self.question

    # check 
    def save(self, *args, **kwargs):
        chapter_id = self.chapter.id # Gets the related chapter's ID
        chapter = Chapter.objects.get(id=chapter_id) # Fetches the chapter instance
        self.chapter_no = chapter.chapter_no # Sets the chapter number
        super(Question, self).save(*args, **kwargs) # Calls the parent save method

    class Meta:
        ordering = ('grade', 'subject', 'chapter', 'question_type', '-created_at')


answer_choices = (
    ("option_a", "option_a"),
    ("option_b", "option_b"),
    ("option_c", "option_c"),
    ("option_d", "option_d"),
)


class Answer(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE, null=True)
    option_a = models.CharField(max_length=50, null=True, blank=True)
    option_b = models.CharField(max_length=50, null=True, blank=True)
    option_c = models.CharField(max_length=50, null=True, blank=True)
    option_d = models.CharField(max_length=50, null=True, blank=True)
    answer = models.CharField(max_length=50, choices=answer_choices, default=answer_choices[0][0])

    def __str__(self):
        return  self.answer
        # return self.question + self.answer
    
# error adding in admin 
class Question_Paper(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    file = models.FileField(upload_to='question_files/', null=True, blank=True)
    created_by = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    test_id = models.CharField(max_length=25, null=True, blank=True)
    no_of_questions = ArrayField(models.CharField(max_length=10, blank=True), blank=True,default=list)
    timing = models.IntegerField(default=0)
    overall_marks = models.IntegerField(default=0)

    def __str__(self):
        return (str(self.grade))+' '+(str(self.subject))
    
    # check
    #     self.created_at = (datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
    # def save(self, *args, **kwargs):
    #     if self.test_id:
    #         test = Test.objects.get(test_id=self.test_id)
    #         test.marks = self.overall_marks
    #         test.duration = self.timing
    #         test.save()
    #     super(Question_Paper, self).save(*args, **kwargs)

    class Meta:
        ordering = ('grade', 'subject', '-created_at',)


class Test(models.Model):
    question_paper = models.ForeignKey(Question_Paper, on_delete=models.SET_NULL, null=True)
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    duration = models.PositiveIntegerField()
    created_staff_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    marks = models.PositiveIntegerField()
    remarks = models.CharField(max_length=25)
    description = models.CharField(max_length=50)
    test_id = models.CharField(max_length=25, null=True, blank=True)
    pass_percentage = models.PositiveIntegerField(default=35)

    def __str__(self):
        return self.test_id 
    #  i got error trying to subject and grade instead of test_id

    # this save doesnt add the values if not given instead it asks to fill the fields, maybe for it to work null=true should be given but please check
    # check
    # def save(self, *args, **kwargs):
    #     if not self.test_id:
    #         self.test_id = (str(uuid.uuid4()))[:16]  # Generates a 16-character UUID
    #     question_paper = self.question_paper  # Retrieves the related question paper
    #     if not self.duration:
    #         self.duration = question_paper.timing  # Sets the duration from the question paper
    #     if not self.marks:
    #         self.marks = question_paper.overall_marks  # Sets the marks from the question paper
    #     super(Test, self).save(*args, **kwargs)  # Calls the parent save method

    class Meta:
        ordering = ('grade', 'subject', 'created_staff_id', 'question_paper')


class TestResult(models.Model):
    student_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    test_id = models.ForeignKey(Test, on_delete=models.DO_NOTHING, null=True)
    question_paper = models.ForeignKey(Question_Paper, on_delete=models.DO_NOTHING, null=True)
    result = models.CharField(max_length=50)
    score = models.PositiveIntegerField()
    correct_answer = models.IntegerField(null=True)
    wrong_answer = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    unanswered_questions = models.IntegerField(null=True)
    test_detail = jsonfield.JSONField()

    def __str__(self):
        return self.result

    
class InstructionForTest(models.Model):
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.note[:10])


class Questionbank(models.Model):
    question_file = models.FileField(upload_to='question_files/', null=True, blank=True)
    # answer_file=models.FileField(upload_to='answer_files/',null=True,blank=True)
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.question_file)
