from ast import List
from base64 import standard_b64decode
from operator import truediv
from os import stat
import json
from utils.pagination import Pagination
from itertools import chain
from pickle import TRUE
from re import sub
# from matplotlib import test
from django.db.models import Count
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView,
    ListAPIView,
    RetrieveDestroyAPIView,
)
from utils.response import ResponseChoices
from accounts.permission import IsAdminUser, IsStaffUser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED, HTTP_206_PARTIAL_CONTENT,
    HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_203_NON_AUTHORITATIVE_INFORMATION, HTTP_204_NO_CONTENT, HTTP_422_UNPROCESSABLE_ENTITY
)
from .forms import *
from django.conf import settings
from django.core.mail import send_mail
import random
from django.shortcuts import render
from .serializers import (
    SubjectSerializer,
    ChapterSerializer,
    GradeSerializer,
    ChapterViewSerializer,
    QuestionAnswerSerializer,
    QuestionGetSerializer,
    QuestionSerializer,
    QuestionPaperSerializer,
    TestSerializer,
    TestResultSerializer,
    TestInstruction,
)
from .models import Question, Subject, Grade, Chapter, Question_Paper, Answer, Questionbank, Test, TestResult
from accounts.models import User
# from .utils import render_to_pdf, render_to_pdf2
from utils.pagination import Pagination
from rest_framework.authentication import TokenAuthentication


'''
difference bw get retrieve list, put patch 
'''


class GradeView(ListCreateAPIView):
    serializer_class = GradeSerializer
    queryset = Grade.objects.all().order_by('grade')
    permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [AllowAny]

    def list(self, request):
        user = self.request.user
        queryset = self.get_queryset()

        # if user.is_anonymous:
        #     queryset = Grade.objects.all()
        if user.user_type == "is_admin":
            queryset = Grade.objects.all()

        elif user.user_type == 'is_staff':
            grade = user.profile.standard
            grade_list = []
            for i in grade:
                # grade_list.append(int(i[0]))
                grade_list.append(int((i.split('-'))[0]))
            print(grade, grade_list)
            queryset = queryset.filter(grade__in=grade_list)
        elif user.user_type == 'is_student':
            return Response({"status": Response.FAILURE, 'data': 'Your not have access to view this page'})
        serializer = GradeSerializer(queryset, many=True)
        return Response({"status": ResponseChoices.SUCCESS, 'data': serializer.data})
    
    def create(self, request):
        serializer = GradeSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": ResponseChoices.SUCCESS, 'data': serializer.data}, status=HTTP_201_CREATED)
        return Response({"status": ResponseChoices.FAILURE, "data": serializer.errors}, status=HTTP_206_PARTIAL_CONTENT)

        
class GradeEditView(RetrieveUpdateDestroyAPIView):

    # permission_classes = [AllowAny]
    permission_classes = [IsAuthenticated]
    serializer_class = GradeSerializer
    queryset = Grade.objects.all().order_by('grade')

    # def retrieve(self, request, *args, **kwargs):
    #     return super().retrieve(request, *args, **kwargs)

    def retrieve(self, request, pk):
        try:
            queryset = Grade.objects.get(pk=pk)
        except:
            return Response({'status': 'failure', "data": "Grade doesn't exists"}, status=HTTP_206_PARTIAL_CONTENT)
        serializer = GradeSerializer(queryset)
        return Response(serializer.data, status=HTTP_200_OK)

    def patch(self, request, pk):
        subject = Grade.objects.get(pk=pk)
        serializer = GradeSerializer(subject, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": ResponseChoices.SUCCESS, 'data': serializer.data}, status=HTTP_200_OK)
        return Response({"status": ResponseChoices.FAILURE, "data": serializer.errors}, status=HTTP_206_PARTIAL_CONTENT)


class SubjectCreateView(ListCreateAPIView, Pagination):
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all().order_by('grade', 'code')
    permission_classes = [IsAuthenticated]
    # pagination_class = Paginate

    def list(self, request):
        queryset = self.get_queryset()
        grade = self.request.query_params.get('grade')
        if grade is not None:
            try:
                grades = Grade.objects.get(grade=grade)
                queryset = (queryset.filter(grade=grades.id).order_by('code'))
            except Exception as e:
                return Response({"status":  ResponseChoices.FAILURE, 'data': str(e)}, status=HTTP_206_PARTIAL_CONTENT)
        data = self.paginate_queryset(queryset)
        serializer = SubjectSerializer(data, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # if self.request.user.user_type == 'is_staff':
            #     user = self.request.user
            #     gradeid = serializer.data['grade']
            #     grade = Grade.objects.get(id=gradeid)
            #     subjects = serializer.data['name']
            #     admin = User.objects.get(user_type='is_admin')
            #     subject = 'Subject creation'
            #     message = f'{user.profile.full_name} HAD CREATED,ON GRADE : {grade.grade} SUBJECT : {subjects}'
            #     email_from = settings.EMAIL_HOST_USER
            #     recipient_list = [admin.email, ]
            #     send_mail(subject, message, email_from, recipient_list)
            return Response({"status":  ResponseChoices.SUCCESS, 'data': serializer.data}, status=HTTP_201_CREATED)
        return Response({"status": ResponseChoices.FAILURE, "data": serializer.errors}, status=HTTP_206_PARTIAL_CONTENT)


class SubjectEditView(RetrieveUpdateDestroyAPIView):
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]
    queryset = Subject.objects.all().order_by('grade', 'code')

    def retrieve(self, request, pk):
        try:
            queryset = Subject.objects.get(pk=pk)
        except:
            return Response({'status': 'failure', "data": "Subject doesn't exists"}, status=HTTP_206_PARTIAL_CONTENT)
        serializer = SubjectSerializer(queryset)
        return Response(serializer.data, status=HTTP_200_OK)

    def update(self, request, pk):
        subject = Subject.objects.get(pk=pk)
        serializer = SubjectSerializer(subject, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": ResponseChoices.SUCCESS, 'data': serializer.data}, status=HTTP_200_OK)
        return Response({"status": ResponseChoices.FAILURE, "data": serializer.errors}, status=HTTP_206_PARTIAL_CONTENT)
    

class ChaptersCreateView(CreateAPIView, Pagination):

    permission_classes = [IsAuthenticated]
    serializer_class = ChapterSerializer
    queryset = Chapter.objects.all().order_by('subject', 'chapter_no')

    def get(self, format=None):
        queryset = Chapter.objects.all().order_by('subject', 'chapter_no')
        data = self.paginate_queryset(queryset)
        serializer = ChapterSerializer(data, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = ChapterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": ResponseChoices.SUCCESS, 'data': serializer.data}, status=HTTP_201_CREATED)
        return Response({"status":  ResponseChoices.FAILURE, "data": serializer.errors}, status=HTTP_206_PARTIAL_CONTENT)


class ChapterEditView(RetrieveUpdateDestroyAPIView):

    serializer_class = ChapterSerializer
    permission_classes = [IsAuthenticated]
    queryset = Chapter.objects.all().order_by('subject', 'chapter_no')

    # difference get, list, retrieve 
    def retrieve(self, request, pk):
        try:
            queryset = Chapter.objects.get(pk=pk)
        except:
            return Response({'status': ResponseChoices.FAILURE, "data": "Chapter doesn't exists"}, status=HTTP_206_PARTIAL_CONTENT)
        serializer = ChapterSerializer(queryset)
        return Response(serializer.data)

    def update(self, request, pk):
        subject = Chapter.objects.get(pk=pk)
        serializer = ChapterSerializer(subject, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": ResponseChoices.SUCCESS, 'data': serializer.data}, status=HTTP_200_OK)
        return Response({"status": ResponseChoices.FAILURE, "data": serializer.errors}, status=HTTP_206_PARTIAL_CONTENT)
    

class ChapterListView(APIView):
    serializer_class = ChapterViewSerializer
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]

    def post(self, request):
        grade = request.data.get('grade')
        subject = (request.data.get('subject')).upper() # upper?
        try:
            if subject:
                data = []
                grade = Grade.objects.get(grade=grade)
                subject = Subject.objects.get(name=subject, grade=grade.id)
                chapters = (Chapter.objects.filter(subject=subject)
                            ).order_by('subject', 'chapter_no')
                for object in chapters:
                    data.append({
                        "id": object.id,
                        "subject": subject.name,
                        "subject_id": subject.id,
                        "grade": subject.grade.grade,
                        "name": object.name,
                        "chapter_no": object.chapter_no,
                        "description": object.description,
                    })
            if len(data):
                return Response({"status": ResponseChoices.SUCCESS, 'data': data})
        except:
            return Response({"status": "Not found"}, status=HTTP_206_PARTIAL_CONTENT)
        return Response({"status": ResponseChoices.FAILURE}, status=HTTP_206_PARTIAL_CONTENT)

# check
# class SubjectListView(ListAPIView, Pagination):
#     serializer_class = SubjectSerializer
#     permission_classes = [AllowAny]

#     #  understand the difference of get and list 
#     def get_queryset(self):
#         queryset = Subject.objects.all()
#         grade = self.request.query_params.get('grade')
#         if grade is not None:
#             try:
#                 grades = Grade.objects.get(grade=grade)
#                 queryset = (queryset.filter(grade=grades.id).order_by('code'))
#             except:
#                 return Response({'status': ResponseChoices.FAILURE}, status=HTTP_206_PARTIAL_CONTENT)
#             return queryset

#     def list(self, request):
#         queryset = self.get_queryset()
#         data = self.paginate_queryset(queryset)
#         serializer = SubjectSerializer(data, many=True)
#         return self.get_paginated_response(serializer.data)

class SubjectListView(ListAPIView, Pagination):
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]
   
    def get_queryset(self):
        queryset = Subject.objects.all()
        grade = self.request.query_params.get('grade')
        if grade:
            try:
                grades = Grade.objects.get(grade=grade)
                queryset = queryset.filter(grade=grades.id).order_by('code')
            except Grade.DoesNotExist:
                queryset = Subject.objects.none()  # Return an empty queryset
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = self.paginate_queryset(queryset)
        if data is not None:  # Ensure data is not None before serialization
            serializer = self.get_serializer(data, many=True)
            return self.get_paginated_response(serializer.data)
        return self.get_paginated_response([])  # Return an empty response if no data



# isnt it shoul dbe ListCreateAPIView
class QuestionCreateView(CreateAPIView, Pagination):
    serializer_class = QuestionAnswerSerializer
    queryset = Question.objects.all().order_by('grade', 'subject', 'chapter')
    permission_classes = [IsAuthenticated]

    def get(self, request):
        grade = self.request.query_params.get('grade')
        subject = self.request.query_params.get('subject')
        from_chapter_no = self.request.query_params.get('from_chapter_no')
        to_chapter_no = self.request.query_params.get('to_chapter_no')
        questions = Question.objects.all()
        data = self.paginate_queryset(questions)
        if grade and subject:
            try:
                # check the query
                if from_chapter_no and to_chapter_no:
                    questions = Question.objects.filter(grade_id=int(grade), subject_id=int(
                        subject), chapter_no__gte=from_chapter_no, chapter_no__lte=to_chapter_no)
                else:
                    questions = Question.objects.filter(
                        grade_id=int(grade), subject_id=int(subject))
            except:
                # questions = Question.objects.all()
                return Response({'status': Response.FAILURE, 'data': 'give a valid grade and subject'}, status=HTTP_206_PARTIAL_CONTENT)
        if len(questions):
            serializer = QuestionAnswerSerializer(data, many=True)
            return self.get_paginated_response(serializer.data)
        return Response({'status': ResponseChoices.FAILURE, 'data': "subject don't have a questions"}, status=HTTP_206_PARTIAL_CONTENT)

    def post(self, request):
        serializer = QuestionAnswerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": ResponseChoices.SUCCESS, 'data': serializer.data}, status=HTTP_201_CREATED)
        return Response({"status": ResponseChoices.FAILURE, "data": serializer.errors}, status=HTTP_206_PARTIAL_CONTENT)


class QuestionEditView(RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionAnswerSerializer
    permission_classes = [IsAuthenticated]
    # use of queryset
    queryset = Question.objects.all()

    def retrieve(self, request, pk):
        try:
            question = Question.objects.get(pk=pk)
            serializer = QuestionAnswerSerializer(question)
            return Response({"status": ResponseChoices.SUCCESS, 'data': serializer.data}, status=HTTP_200_OK)
        except:
            return Response({'status': ResponseChoices.FAILURE, "data": "Question doesn't exists"}, status=HTTP_206_PARTIAL_CONTENT)


# check
# class QuestionList(APIView):
#     serializer_class = QuestionGetSerializer
#     permission_classes = [AllowAny]

#     def post(self, request):
#         type = str(self.request.query_params.get('type'))
#         grade = request.data.get('grade')
#         subject = (request.data.get('subject'))
#         timing = request.data.get('timing')
#         overall_marks = request.data.get('overall_marks')
#         list_of_questions = request.data.get('list_of_questions')
#         # print(list_of_questions)
#         # print(timing,overall_marks)
#         customize = request.data.get('customize')
#         question_details_list = []
#         print(customize)
#         # list_of_questions = [126,168,132,24,62]

#         if timing:
#             timing = int(timing)
#         if overall_marks:
#             overall_marks = int(overall_marks)
#         try:
#             grade = Grade.objects.get(grade=grade)
#             subject_obj = Subject.objects.get(id=subject)
#             user = self.request.user
#             questions = []
#             if customize:
#                 print('hi')
#                 customize = json.loads(customize)
#                 for i in customize:
#                     print(i)
#                     chapter = Chapter.objects.get(id=i['id'])
#                     for j in i['cognitive_level']:
#                         try:
#                             cognitive = j.capitalize()
#                             newlist = Question.objects.filter(
#                                 chapter=chapter.id, cognitive_level=cognitive)
#                             newlist = (
#                                 sorted(newlist, key=lambda x: random.random()))
#                             num = int(i['cognitive_level'][j])
#                             if len(newlist) >= num:
#                                 newlist = newlist[:num]
#                                 questions.append(newlist)
#                             else:
#                                 return Response({'status': Response.FAILURE, 'data': ('Required questions not available in {} level in chapter {}. Available number of questions is {}').format(cognitive, chapter, len(newlist))}, status=HTTP_206_PARTIAL_CONTENT)
#                         except:
#                             return Response({"status": Response.FAILURE, "data": "given details are incorrect"}, status=HTTP_206_PARTIAL_CONTENT)
#                 questions = [item for sublist in questions for item in sublist]
#             else:
#                 for i in list_of_questions:
#                     try:
#                         j = Question.objects.get(id=i)
#                         questions.append(j)
#                     except:
#                         continue
#             serializer = QuestionSerializer(questions, many=True)
#             serializer_for_questions = QuestionAnswerSerializer(
#                 questions, many=True)
#             type = type.lower()
#             # answers
#             answers = []
#             question_list = []
#             for question in questions:
#                 ans = getattr(question.answers, str(question.answers))
#                 question_list.append(question.question)
#                 answers.append(ans)
#             context = {'data': serializer.data, 'grade': grade.grade,
#                        'subject': subject_obj.name, 'register_number': user.register_number}
#             context1 = {'data': serializer.data, 'grade': grade.grade, 'subject': subject_obj.name,
#                         'register_number': user.register_number, 'answers': answers}
#             answer_file, status = render_to_pdf2(
#                 'academics/answer_file.html', 'answer_files', None, context1)
#             # save question_paper in data_base
#             if type == 'save':
#                 cal_timing = 0
#                 cal_overall_marks = 0
#                 for i in questions:
#                     print(int(i.duration))
#                     cal_timing += int(i.duration)
#                     cal_overall_marks += int(i.mark)
#                 if not timing:
#                     timing = cal_timing
#                 if not overall_marks:
#                     overall_marks = cal_overall_marks
#                 created_by = self.request.user.email
#                 question_paper = Question_Paper.objects.create(
#                     grade=grade, subject=subject_obj, created_by=created_by, timing=timing, overall_marks=overall_marks)
#                 print(question_paper)
#                 for question in questions:
#                     question_paper.no_of_questions.append(question.id)
#                 question_paper, status = render_to_pdf2(
#                     'academics/question.html', 'question_files', question_paper, context)
#                 if not status:
#                     return Response({"status": ResponseChoices.FAILURE, "data": "given details are incorrect"}, status=HTTP_206_PARTIAL_CONTENT)
#                 serializer = QuestionPaperSerializer(question_paper)
#                 return Response({'status': ResponseChoices.SUCCESS, 'data': serializer.data, 'question_details': serializer_for_questions.data, 'questions': question_list, 'answer-file-path': '/media/answer_files/{answer_file}.pdf', 'subject_id': subject_obj.id, 'grade_id': grade.id}, status=HTTP_200_OK)
#             filename, status = render_to_pdf2(
#                 'academics/question.html', 'question_paper', None, context)
#             if not status:
#                 return Response({"status": ResponseChoices.FAILURE, "data": "given details are incorrect"}, status=HTTP_206_PARTIAL_CONTENT)
#             return Response({'status': ResponseChoices.SUCCESS, 'question_path': f'/media/question_paper/{filename}.pdf', 'answer_path': f'/media/answer_files/{answer_file}.pdf', 'subject_id': subject_obj.id, 'grade_id': grade.id})
#         except:
#             return Response({"status": ResponseChoices.FAILURE, "data": "given details are incorrect"}, status=HTTP_206_PARTIAL_CONTENT)
        

class QuestionPaperList(ListAPIView, Pagination):
    serializer_class = QuestionPaperSerializer
    permission_classes = [IsAuthenticated]
    queryset = Question_Paper.objects.all().order_by('grade', 'subject')

    def get(self, request):

        grade = (self.request.query_params.get('grade'))
        subject = (str(self.request.query_params.get('subject'))).upper()
        if grade:
            grade = Grade.objects.get(grade=grade)
            try:
                subject = Subject.objects.get(grade=grade.id, name=subject)
                questions = Question_Paper.objects.filter(
                    grade=grade.id, subject=subject.id)
            except:
                questions = Question_Paper.objects.filter(grade=grade.id)
        else:
            questions = Question_Paper.objects.all()
        data = self.paginate_queryset(questions)
        serializer = QuestionPaperSerializer(data, many=True)

        return self.get_paginated_response(serializer.data)

#  check
# class QuestionPaperView(RetrieveUpdateDestroyAPIView):
#     serializer_class = QuestionPaperSerializer
#     permission_classes = [AllowAny]
#     queryset = Question_Paper.objects.all()

#     def retrieve(self, request, pk):
#         try:
#             question_paper = Question_Paper.objects.get(pk=pk)
#             serializer = QuestionPaperSerializer(question_paper)
#             type = (self.request.query_params.get('type'))
#             if type != None and (type).lower() == 'file':
#                 answers_list = []
#                 questions = question_paper.no_of_questions
#                 for question in questions:
#                     question_from_model = Question.objects.get(id=question)
#                     answers = Answer.objects.get(question=question_from_model)
#                     answer = answers.answer
#                     if answers.question.question_type == 'Fill_in_the_blanks':
#                         answer = getattr(answers, str(answer))
#                     answers_list.append(answer)
#                 user = self.request.user
#                 context = {'answers': answers_list, 'grade': question_paper.grade.grade,
#                            'subject': question_paper.subject.name, 'register_number': user.register_number}
#                 filename, status = render_to_pdf2(
#                     'academics/answer_file.html', 'answer_files', None, context)
#                 if not status:
#                     return Response({'status': 'given details incorrect'}, status=HTTP_200_OK)
#                 return Response({'path': f'/media/answer_files/{filename}.pdf', 'data': serializer.data}, status=HTTP_200_OK)
#             return Response({'status': ResponseChoices.SUCCESS, 'data': serializer.data}, status=HTTP_200_OK)
#         except:
#             return Response({"status": ResponseChoices.FAILURE, "data": "Question-paper doesn't exists"}, status=HTTP_206_PARTIAL_CONTENT)

#     def patch(self, request, pk):
#         question_paper = Question_Paper.objects.get(pk=pk)
#         serializer = QuestionPaperSerializer(
#             question_paper, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"status": ResponseChoices.SUCCESS, 'data': serializer.data}, status=HTTP_200_OK)
#         return Response({"status": ResponseChoices.FAILURE, "data": serializer.errors}, status=HTTP_206_PARTIAL_CONTENT)


class QuestionFromQuestionPaper(APIView):
    serializer_class = QuestionAnswerSerializer
    queryset = Question.objects.all().order_by('grade', 'subject', 'chapter')
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        question_paper_id = (self.request.query_params.get('question_paper'))
        question_paper = Question_Paper.objects.get(id=question_paper_id)
        question_list = question_paper.no_of_questions
        data = []
        change = False
        for i in question_list:
            try:
                queryset = Question.objects.get(id=int(i))
                data.append((QuestionAnswerSerializer(queryset)).data)
            except:
                question_list.remove(i)
                change = True
        if change:
            question_paper.no_of_questions = question_list
            question_paper.save()
        return Response(data)


class TestCreateView(CreateAPIView):
    serializer_class = TestSerializer
    queryset = Test.objects.all().order_by('grade', 'subject')
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        grade = (self.request.query_params.get('grade'))
        test_id = (self.request.query_params.get('test_id'))
        if grade:
            queryset = Test.objects.filter(grade=grade)
            data = self.paginate_queryset(queryset)
            serializer = TestSerializer(data, many=True)
            # serializer = TestSerializer(queryset, many=True)
        if test_id:
            try:
                queryset = Test.objects.get(test_id=test_id)
                print(queryset)
                serializer = TestSerializer(queryset)
                print(serializer)
                return Response({'status': ResponseChoices.SUCCESS, 'data': serializer.data}, status=HTTP_200_OK)
            except:
                return Response({"status": "failure", "data": "please give a valid test id"}, status=HTTP_206_PARTIAL_CONTENT)

        else:
            queryset = Test.objects.all().order_by('grade', 'subject')
            data = self.paginate_queryset(queryset)
            serializer = TestSerializer(data, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = TestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            question_paper = request.data['question_paper']
            Test_obj = Test.objects.get(question_paper=question_paper)
            question_paper = Question_Paper.objects.get(id=question_paper)
            question_paper.test_id = Test_obj.test_id
            question_paper.save()

            return Response({"status": ResponseChoices.SUCCESS, 'data': serializer.data}, status=HTTP_201_CREATED)
        return Response({"status": ResponseChoices.FAILURE, "data": serializer.errors}, status=HTTP_206_PARTIAL_CONTENT)


class TestEditView(RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    # necessary
    serializer_class = TestSerializer
    queryset = Test.objects.all().order_by('grade', 'subject')

    def retrieve(self, request, pk):
        try:
            queryset = Test.objects.get(pk=pk)
        except:
            return Response({'status': 'failure', "data": "Test doesn't exists"}, status=HTTP_206_PARTIAL_CONTENT)
        serializer = TestSerializer(queryset)
        return Response(serializer.data, status=HTTP_200_OK)

    def update(self, request, pk):
        test = Test.objects.get(pk=pk)
        serializer = TestSerializer(test, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": ResponseChoices.SUCCESS, 'data': serializer.data}, status=HTTP_200_OK)
        return Response({"status": ResponseChoices.FAILURE, "data": serializer.errors}, status=HTTP_206_PARTIAL_CONTENT)

    def destroy(self, request, pk, *args, **kwargs):
        test = Test.objects.get(id=pk)
        test_id = test.test_id
        question_paper = Question_Paper.objects.get(test_id=test_id)
        question_paper.test_id = None
        question_paper.save()
        # super? 
        return super(TestEditView, self).destroy(request, *args, **kwargs)


class TestResultCreateView(CreateAPIView):
    serializer_class = TestResultSerializer
    queryset = TestResult.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        queryset = TestResult.objects.all()
        grade = self.request.query_params.get('grade')
        student = self.request.query_params.get('student_id')
        test_id = self.request.query_params.get('test_id')
        if grade:
            if student:
                try:
                    grade = Grade.objects.get(grade=grade)
                    queryset = TestResult.objects.filter(
                        grade=grade, student_id=student)
                except:
                    queryset = TestResult.objects.all()
            else:
                try:
                    grade = Grade.objects.get(grade=grade)
                    queryset = TestResult.objects.filter(grade=grade)
                except:
                    return Response({"status": ResponseChoices.FAILURE, 'data': serializer.errors}, status=HTTP_206_PARTIAL_CONTENT)
        elif test_id:
            queryset = TestResult.objects.filter(test_id=test_id)
        queryset = TestResult.objects.all()
        # queryset = queryset.order_by('grade', 'subject')
        print(type(queryset))
        data = self.paginate_queryset(queryset)
        serializer = TestResultSerializer(data, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = TestResultSerializer(data=request.data)
        # customize = json.loads(request.data['test_detail'])
        # for i in customize:
        #     print(i)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": ResponseChoices.SUCCESS, 'data': serializer.data}, status=HTTP_201_CREATED)
        return Response({"status": ResponseChoices.FAILURE, "data": serializer.errors}, status=HTTP_206_PARTIAL_CONTENT)


class TestResultEditView(RetrieveDestroyAPIView):
    # is serializer class and queryset required
    serializer_class = TestResultSerializer
    permission_classes = [IsAuthenticated]
    queryset = TestResult.objects.all()

    def retrieve(self, request, pk):
        try:
            queryset = TestResult.objects.get(pk=pk)
        except:
            return Response({'status': 'failure', "data": "Test result doesn't exists"}, status=HTTP_206_PARTIAL_CONTENT)
        serializer = TestResultSerializer(queryset)
        return Response(serializer.data, status=HTTP_200_OK)


class TestInstructionView(ListCreateAPIView):
    serializer_class = TestInstruction
    queryset = InstructionForTest.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = InstructionForTest.objects.all()
        data = self.paginate_queryset(queryset)
        serializer = TestInstruction(data, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = TestInstruction(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":  ResponseChoices.SUCCESS, 'data': serializer.data}, status=HTTP_201_CREATED)
        return Response({"status": Response.FAILURE, "data": serializer.errors}, status=HTTP_206_PARTIAL_CONTENT)
    
        


class EditTestInstructionView(RetrieveUpdateDestroyAPIView):
    serializer_class = TestInstruction
    queryset = InstructionForTest.objects.all()
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk):
        try:
            queryset = InstructionForTest.objects.get(id=pk)
        except:
            return Response({'status': 'failure', "data": "Instruction doesn't exists"}, status=HTTP_206_PARTIAL_CONTENT)
        serializer = TestInstruction(queryset)
        return Response(serializer.data, status=HTTP_200_OK)


def load_subject_chapter(request):
    grade_id = request.GET.get('grade', None)
    subject_id = request.GET.get('subject', None)
    if grade_id:
        subject = Subject.objects.filter(grade=grade_id).order_by('name')
        return render(request, 'academics/dropdown_list_options.html', {'items': subject})
    chapter = Chapter.objects.filter(subject=subject_id)
    return render(request, 'academics/dropdown_list_options.html', {'items': chapter})


def load_grade(request):
    user = request.user
    print(user)
    if user.user_type == 'is_admin':
        grades = Grade.objects.all()
    elif user.user_type == 'is_staff':
        standard = user.profile.standard
        grades = Grade.objects.filter(grade=standard)
    else:
        return None
    return render(request, 'academics/dropdown_grade.html', {'items': grades})


def load_test(request):
    # grade_id = request.GET.get('grade', None)
    subject_id = request.GET.get('subject', None)
    if subject_id:
        test = Test.objects.filter(subject_id=subject_id)
    return render(request, 'academics/test_dropdown.html', {'items': test})


def load_chapter_no(request):
    subject_id = request.GET.get('subject', None)
    chapter = Chapter.objects.filter(subject=subject_id)
    return render(request, 'academics/dropdown_chapter_no.html', {'items': chapter})
