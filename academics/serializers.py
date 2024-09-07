from curses.ascii import isalpha
from dataclasses import field
from operator import sub 
from pyexpat import model 
from collections import OrderedDict
from rest_framework import serializers, pagination 
from rest_framework.response import Response
import re
from .models import Grade, Question_Paper, Subject, Chapter, Answer, Question, Test, TestResult, InstructionForTest



class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'

    def validate(self, data):
        if not self.instance:
            if Grade.objects.filter(grade=data['grade']).exists():
                raise serializers.ValidationError({'error': 'grade altready exists'})
        return data
    

class SubjectSerializer(serializers.ModelSerializer):
    grade_name = serializers.SerializerMethodField('get_grade_name')

    class Meta:
        model = Subject
        fields = ['id', 'grade', 'grade_name', 'name', 'code', 'created_at']

    # check
    def get_grade_name(self, subject):
        grade = Grade.objects.get(id=(subject.grade.id))
        return grade.grade
    
    def validate(self, data):
        # Extract the 'name' from the input data
        name = data['name']
        
        # Use regex to split 'name' into individual words and digits (removing special characters)
        name = re.findall(r"[^\W\d_]+|\d+", name)
        
        # Check if the first 3 characters of the 'code' are alphabetical
        if data['code'][:3].isalpha():
            # Use regex to split 'code' into alphabetical and numeric parts
            code = re.match(r"([a-z]+)([0-9]+)", data['code'], re.I)
            
            # If regex finds a match, extract the numeric part of the 'code'
            if code:
                items = code.groups()  # 'items' is a tuple of the matched parts (alphabetic, numeric)
                code = items[1]  # Take the numeric part of the 'code'
        else:
            # If the 'code' doesn't start with letters, just use the 'code' as it is
            code = data['code']

        # Format the 'name': join the split parts (e.g., words and numbers), convert to uppercase
        data['name'] = (' '.join(name)).upper()

        # Create the 'code' by combining the first 3 letters of the formatted 'name' with the numeric 'code'
        data['code'] = (data['name'][:3]) + code

        # Get all existing Subject records from the database for duplicate checks
        queryset = Subject.objects.all()
        
        # If this is an update (self.instance exists), exclude the current subject from the queryset
        if self.instance:
            id = self.instance.id
            queryset = queryset.exclude(id=id)

        # Check if a Subject with the same 'name' and 'grade' already exists (excluding the current instance)
        if queryset.filter(name=data['name'], grade=data['grade']).exists():
            # If a duplicate is found, raise a validation error for 'name'
            raise serializers.ValidationError({'error': 'subject name already exists'})

        # Check if a Subject with the same 'code' already exists
        if queryset.filter(code=code).exists():
            # If a duplicate 'code' is found, raise a validation error for 'code'
            raise serializers.ValidationError({'error': 'subject code already exists'})

        # If everything is valid, return the modified and validated 'data'
        return data


class ChapterSerializer(serializers.ModelSerializer):
    subject_name = serializers.SerializerMethodField('get_subject_name')

    class Meta:
        model = Chapter
        fields = ['id', 'subject', 'subject_name', 'name', 'chapter_no', 'description', 'created_at']
        
    def get_subject_name(self, chapter):
        #   subject = Subject.objects.get(id=(chapter.subject_id))
        print(chapter.subject)
        return (chapter.subject.name)
    
    def validate(self, data):
        name = data['name']
        name = re.findall(r"[^\W\d_]+|\d+", name)
        data['name'] = (' '.join(name)).lower()
        queryset = Chapter.objects.all()
        if self.instance:
            id = self.instance.id
            queryset = queryset.exclude(id=id)

        if queryset.filter(name=data['name'], subject=data['subject']).exists():
            raise serializers.ValidationError({'error': 'chapter name already exists'})
        if queryset.filter(subject=data['subject'], chapter_no=data['chapter_no']).exists():
            raise serializers.ValidationError({'error': 'chapter no already exists'})
        return data


class ChapterViewSerializer(serializers.Serializer):
    grade = serializers.IntegerField()
    subject = serializers.CharField()


class Question_answer_serializer(serializers.Serializer):
    grade = serializers.StringRelatedField(many=True, source="Grade")


class questionanswerserializer(serializers.ModelSerializer):
    subject = serializers.SlugRelatedField(slug_field='name', queryset=Subject.objects.all())
    grade = serializers.SlugRelatedField(slug_field='grade', queryset=Grade.objects.all())
    chapter = serializers.SlugRelatedField(slug_field='name', queryset=Chapter.objects.all())

    class Meta:
        model = Question
        fields = ['id', 'grade', 'subject', 'chapter']


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ['option_a', 'option_b', 'option_c', 'option_d', 'answer']


class QuestionAnswerSerializer(serializers.ModelSerializer):
    grade_name = serializers.SerializerMethodField('get_grade_name')
    subject_name = serializers.SerializerMethodField('get_subject_name')
    chapter_name = serializers.SerializerMethodField('get_chapter_name')

    def get_grade_name(self, question):
        return question.grade.grade

    def get_subject_name(self, question):
        return question.subject.name

    def get_chapter_name(self, question):
        return question.chapter.name

    # def get_chapter_name(self,chapter)
    # answers = AnswerSerializer()

    class Meta:
        model = Question
        fields = ['id', 'grade', 'grade_name', 'subject', 'subject_name', 'chapter', 'chapter_name', 'question',
                'question_type', 'cognitive_level', 'difficulty_level', 'mark', 'duration', ]
        # fields = ['id', 'grade', 'grade_name', 'subject', 'subject_name', 'chapter', 'chapter_name', 'question',
        #         'question_type', 'cognitive_level', 'difficulty_level', 'mark', 'duration', 'answers']

    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        question = Question.objects.create(**validated_data)
        Answer.objects.create(question=question, **answers_data)
        return question

    def update(self, instance, validated_data):
        answers_data = validated_data.pop('answers')
        answers = instance.answers

        instance.grade = validated_data.get('grade', instance.grade)
        instance.subject = validated_data.get('subject', instance.subject)
        instance.chapter = validated_data.get('chapter', instance.chapter)
        instance.question = validated_data.get('question', instance.question)
        instance.question_type = validated_data.get('question_type', instance.question_type)
        instance.cognitive_level = validated_data.get('cognitive_level', instance.cognitive_level)
        instance.difficulty_level = validated_data.get('difficulty_level', instance.difficulty_level)
        instance.save()

        answers.answer = answers_data.get('answer', answers.answer)
        answers.option_a = answers_data.get('option_a', answers.option_a)
        answers.option_b = answers_data.get('option_b', answers.option_b)
        answers.option_c = answers_data.get('option_c', answers.option_c)
        answers.option_d = answers_data.get('option_d', answers.option_d)
        answers.save()

        return instance


# check 
# Question_Paper doesn't directly relate to Chapter, both are indirectly related via the Subject model

# It's not wrong to use PrimaryKeyRelatedField for from_chapter in the serializer even though there is no direct relationship between Question_Paper and Chapter
# However, if you want to ensure that the chapters selected for the Question_Paper are related to the same subject, you'll need to add some additional logic to filter the Chapter queryset based on the subject field of the Question_Paper




# the constructor function runs first and assigns a value to the from_chapter and last_chapter with valid choices for chapters. and the user will get the option to choose from these choices 
class QuestionGetSerializer2(serializers.ModelSerializer):
    # subject_name = serializers.CharField()
    from_chapter = serializers.PrimaryKeyRelatedField(queryset=Chapter.objects.all(), default=None)
    to_chapter = serializers.PrimaryKeyRelatedField(queryset=Chapter.objects.all(), default=None)
    number_of_questions = serializers.IntegerField()
    all_chapters = serializers.BooleanField(required=False)
    customize = serializers.JSONField(required=False)

    class Meta:
        model = Question_Paper
        fields = ['grade', 'subject', 'number_of_questions', 'from_chapter',
                  'to_chapter', 'all_chapters', 'timing', 'overall_marks', 'customize']
        
    def __init__(self, *args, **kwargs):
        super(QuestionGetSerializer2, self).__init__(*args, **kwargs)
        subject = self.initial_data.get('subject')  # Get the subject from initial data
        if subject:
            self.fields['from_chapter'].queryset = Chapter.objects.filter(subject=subject)
            self.fields['to_chapter'].queryset = Chapter.objects.filter(subject=subject)
        

class QuestionGetSerializer(serializers.ModelSerializer):
    # subject_name = serializers.CharField()
    # number_of_questions = serializers.IntegerField()
    # all_chapters = serializers.BooleanField(required=False)
    # to_chapter = serializers.PrimaryKeyRelatedField(queryset=Chapter.objects.all(),default=None)
    # from_chapter = serializers.PrimaryKeyRelatedField(queryset=Chapter.objects.all(),default=None)
    customize = serializers.JSONField(required=False)
    list_of_questions = serializers.ListField()

    class Meta:
        model = Question_Paper
        fields = ['grade', 'subject', 'timing', 'overall_marks', 'customize', 'list_of_questions']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class QuestionPaperSerializer(serializers.ModelSerializer):
    grade_name = serializers.SerializerMethodField('get_grade_name')
    subject_name = serializers.SerializerMethodField('get_subject_name')

    def get_grade_name(self, subject):
        grade = Grade.objects.get(id=(subject.grade.id))
        return grade.grade

    def get_subject_name(self, chapter):
        subject = Subject.objects.get(id=(chapter.subject.id))
        return subject.name

    class Meta:
        model = Question_Paper
        fields = ['id', 'grade', 'grade_name', 'subject', 'subject_name', 'file',  'test_id',
                'no_of_questions', 'overall_marks', 'timing', 'created_by', 'created_at']
        read_only_fields = ('test_id',)


class TestSerializer(serializers.ModelSerializer):
    grade_name = serializers.SerializerMethodField('get_grade_name')
    subject_name = serializers.SerializerMethodField('get_subject_name')

    def get_grade_name(self, subject):
        print(subject)
        grade = Grade.objects.get(id=(subject.grade.id))
        return grade.grade

    def get_subject_name(self, chapter):
        subject = Subject.objects.get(id=(chapter.subject.id))
        return subject.name

    class Meta:
        model = Test
        fields = ['id', 'grade', 'grade_name', 'subject', 'subject_name', 'question_paper', 'test_id'
                'created_staff_id', 'duration', 'marks', 'pass_percentage', 'remarks', 'description', ]
        read_only_fields = ('test_id',)


class TestResultSerializer(serializers.ModelSerializer):
    subject_name = serializers.SerializerMethodField('get_subject_name')
    # student_name = serializers.SerializerMethodField('get_student')
    register_number = serializers.SerializerMethodField('get_register_no')

    def get_subject_name(self, test):
        print(test.subject.name)
        return test.subject.name

    # def get_student(self, test):
    #     return test.student_id

    def get_register_no(self, test):
        print(test.student_id.register_number, 'here commint')
        return test.student_id.register_number

    class Meta:
        model = TestResult
        fields = ['id', 'grade', 'subject', 'subject_name', 'register_number', 'student_id', 'test_id','question_paper', 
                'result', 'score', 'correct_answer', 'created_at', 'unanswered_questions', 'wrong_answer', 'test_detail']


class TestInstruction(serializers.ModelSerializer):
    class Meta:
        model = InstructionForTest
        fields = '__all__'
