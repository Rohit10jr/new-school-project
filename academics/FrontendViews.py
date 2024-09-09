from multiprocessing import reduction
from urllib import response
from . forms import *
from django.shortcuts import render,redirect
from .models import *
import requests
import json
from django.contrib.auth.decorators import login_required



def gradeview(request): 
            gradeform = grade_form
            subjectform = Subjectform
            chapterform = Chapterform
            return render(request,'academics/grade-subject-chapter.html',{'gradeform':gradeform,'subjectform':subjectform,'chapterform':chapterform})

def questioncreationview(request): 
        form=question_form()
        form1=answer_form()  
        return render(request,'academics/question.html',{'form':form,'form1':form1})

def chapterlistview(request):
        form= form_for_chapterlist()
        form2 = Chapterform()
        return render(request,'academics/chapterlist.html',{'form':form,'form2':form2})
   

def questionlistview(request):   
        form=questionlist_form()
        return render(request,'academics/questionlist.html',{'form':form})
    
def chaptercrud(request):  
        form= chapter_form()
        return render(request,'academics/chapters.html',{'form':form})
   
def subjectcrud(request): 
        form= subject_form()
        return render(request,'academics/subjectcreate.html',{'form':form})


def questionview(request): 
        form = form_for_chapterlist(auto_id='get_%s')
        questionform = Questionform()
        answerform = Answerform()
        return render(request,'academics/questionandanswers.html',{'form':form,'answerform':answerform,'questionform':questionform})
   
def question_paperview2(request):
        form=questionlist_form()
        test_form = TestForm()
        list_form = chapterlist_form()
        custom_form=questionCustomForm()
        form1=customizeForm()
        return render(request,'academics/question_paper_custom.html',{'form':form,'list_form':list_form,'custom_form':custom_form,'form1':form1,'test_form':test_form})
    
def question_paperview(request):
        form=questionlist_form()
        test_form = TestForm()
        list_form = chapterlist_form()
        custom_form=questionCustomForm()
        form1=customizeForm()
        return render(request,'academics/question_paper_customize.html',{'form':form,'list_form':list_form,'custom_form':custom_form,'form1':form1,'test_form':test_form})
  
def questioncreate(request):
 
            questionform = Questionform()
            answerform = Answerform()
            return render(request,'academics/question-by-grade.html',{'answerform':answerform,'questionform':questionform})
def test_create(request):
        form = form_for_chapterlist(auto_id='get_%s')
        test_form = TestForm()
        return render(request,'academics/test-create.html',{'form':form,'test_form':test_form})


def test_list(request):
        return render(request,'academics/student-test-list-page.html')
  
def testhistory(request):
        return render(request,'academics/test-history.html')   
    
def take_test(request,pk):
        return render(request,'academics/take-test.html')


def instruct(request):
        form = instruction_form()
        return render(request,'academics/instruction.html',{'form':form})
   
def questionbank(request):
        return render(request,'academics/question-bank.html')
 
def student_test_history(request):
        form = form_for_chapterlist()
        return render(request,'academics/student-test-history-details.html',{'form':form})
def unknown(request):
     return render(request,'404.html')