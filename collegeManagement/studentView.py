import re
from django.shortcuts import render,HttpResponse, redirect,HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
from .models import *
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from itertools import chain
from asyncio.windows_events import NULL
from django.db.models import Q
from django.db.models import Avg

#  Home
def studentHome(request):
    coursesNum = len(Enrollments.objects.filter(student=Students.objects.get(admin=request.user)))
    student = Students.objects.get(admin=request.user)
    feedbaksNum = len(Feedback.objects.filter(user=request.user))
    lecturesNum = len(Lecture.objects.filter(course__in = Enrollments.objects.filter(student=Students.objects.get(admin=request.user)).values('course')))
    announesNum = len(Announcement.objects.filter(course__in = Enrollments.objects.filter(student=Students.objects.get(admin=request.user)).values('course')))
    ResultsAvg= Result.objects.filter(user= request.user).aggregate(Avg('result'))
    return render(request, 'collegeManagement/students/studentHome.html', 
    {"coursesNum":coursesNum, "student":student, "feedbaksNum":feedbaksNum, "lecturesNum":lecturesNum, "announesNum":announesNum, "ResultsAvg":ResultsAvg})
# courses
def allCourses(request):
    enrolled_courses = Enrollments.objects.filter(student=Students.objects.get(admin=request.user))
    requested_courses = EnrollmentRequests.objects.filter(student=Students.objects.get(admin=request.user))
    resultList = []
    for c in enrolled_courses:
        resultList.append(c.course.id)
    
    for c in requested_courses:
        resultList.append(c.course.id)
    
    print(resultList)
    courses = Course.objects.exclude(id__in=resultList)
    print(courses)

    return render(request, 'collegeManagement/students/courses.html',{"courses":courses})

def enrolledCourses(request):
    enrolled_courses = Enrollments.objects.filter(student=Students.objects.get(admin=request.user)).order_by("-created_at")
    return render(request, 'collegeManagement/students/EnrolledCourses.html',{"enrolled_courses":enrolled_courses})

# enroll
def enroll(request,cid):
    enrollment = EnrollmentRequests(student=Students.objects.get(admin=request.user), course=Course.objects.get(id=cid))
    enrollment.save()
    return redirect("allCourses")
# unenroll
def unenroll(request,cid):
    enrollment = Enrollments.objects.get(student=Students.objects.get(admin=request.user), course=Course.objects.get(id=cid))
    enrollment.delete()
    return redirect("enrolledCourses")

@csrf_exempt
def enrollment(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data.get("name")
        code = data.get("code")
        is_code_exists = Course.objects.filter(code=code).exists()
        if not is_code_exists:
            return JsonResponse({"error": "this course does not exist"}, status=400)
        
        is_request_exists = Enrollments.objects.filter(student=Students.objects.get(admin=request.user), course=Course.objects.get(code=code)).exists()
        if is_request_exists:
            return JsonResponse({"error": "you have already enrolled"}, status=400)

        is_request_exists = EnrollmentRequests.objects.filter(student=Students.objects.get(admin=request.user), course=Course.objects.get(code=code)).exists()
        if is_request_exists:
            return JsonResponse({"error": "you have already enrolled, please wait staff acceptance"}, status=400)
        enrollment = EnrollmentRequests(student=Students.objects.get(admin=request.user), course=Course.objects.get(code=code))
        enrollment.save()
        return JsonResponse({"success": "Enrolled succesfully"}, status=400)
    return render(request, 'collegeManagement/students/enroll.html')

# view Course
def viewCourse(request,cid):
    return render(request, 'collegeManagement/students/viewCourse.html',{"cid":cid})

# lectures
def lectures(request,cid):
    course_lectures = Lecture.objects.filter(course=Course.objects.get(id=cid)).order_by("-created_at")
    return render(request, 'collegeManagement/students/lectures.html', {"course_lectures":course_lectures})

def sannouncements(request,cid):
    course_announcements = Announcement.objects.filter(course=Course.objects.get(id=cid)).order_by("-created_at")
    return render(request, 'collegeManagement/students/sannouncements.html', {"course_announcements":course_announcements})

# Feedback
def studentFeedback(request):
    if request.method == 'POST':
        feedback = Feedback(feedback=request.POST["feedback"], user=request.user)
        feedback.save()
        return redirect('studentFeedback')
    feedback_reply=[]
    feedbacks = Feedback.objects.filter(user=request.user).order_by("-created_at")
    for f in feedbacks:
        try:
            reply = Reply.objects.get(feedback=f)
            feedback_reply.append([f, reply.reply])
        except Reply.DoesNotExist:
            feedback_reply.append([f, "No Reply"])
    return render(request, 'collegeManagement/students/feedback.html', {"feedbacks":feedback_reply})

# apply for leave
def studentLeave(request):
    if request.method == 'POST':
        request = LeaveRequest(reason=request.POST["reason"], user=request.user)
        request.save()
        return redirect('studentLeave')
    return render(request, 'collegeManagement/students/leave.html', {})

# all Announcements
def allAnnouncements(request):
    enrolled_courses = Enrollments.objects.filter(student=Students.objects.get(admin = request.user)).values_list('course', flat=True)
    print(enrolled_courses)
    announcements = Announcement.objects.filter(Q(course__in = enrolled_courses) | Q(course  = NULL)).order_by("-created_at")
    print(announcements)
    return render(request, 'collegeManagement/students/announcments.html', {"announcements":announcements})


# quizes
def studentQuizes(request, cid):
    quizes = Quiz.objects.filter(course = Course.objects.get(id=cid))
    return render(request, 'collegeManagement/students/Studentquizes.html', {"cid":cid, "quizes":quizes})

def studentShowQuiz(request, qid):
    if request.method == 'POST':
        quiz = Quiz.objects.get(id = qid)
        questions = Question.objects.filter(quiz=quiz)
        result = 0
        for question in questions:
            print(request.POST[str(question.id)])
            print(question.right)
            if(question.right == request.POST[str(question.id)]):
                result = result + 1
        result = Result(quiz=quiz, user=request.user, result=result, total= len(questions))
        result.save()
        return redirect("../../results")
    quiz = Quiz.objects.get(id = qid)
    is_result_exists = Result.objects.filter(quiz=quiz, user=request.user).exists()
    if is_result_exists:
        return redirect("../../studentQuizes/"+str(quiz.course.id))
    questions = Question.objects.filter(quiz=quiz)
    questions_options = []
    for question in questions:
        questions_options.append([question, Option.objects.filter(question=question)])
    return render(request, 'collegeManagement/students/StudentShowQuiz.html', {"qid":qid,"questions":questions_options})

# results
def results(request):
    results = Result.objects.filter(user=request.user)
    return render(request, 'collegeManagement/students/results.html', {"results":results})

# studentAppointements
def studentAppointements(request, cid):
    appointements = apointement.objects.filter(course = Course.objects.get(id=cid)).order_by("-created_at")
    return render(request, 'collegeManagement/students/studentAppointements.html', 
    {"appointements":appointements})
