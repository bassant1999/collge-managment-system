from asyncio.windows_events import NULL
from django.shortcuts import render,HttpResponse, redirect,HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login

from collegeManagement.studentView import lectures
from .models import *
from django.contrib import messages
import json
from django.http import JsonResponse
from django.db.models import Q
from django.http import FileResponse
from datetime import datetime
import datetime
from django.views.decorators.csrf import csrf_exempt

# Home
def staffHome(request):
    courses = Course.objects.filter(staff=Staffs.objects.get(admin=request.user))
    coursesNum = len(courses)
    lecturesNum = len(Lecture.objects.filter(course__in = courses))
    studentsNum = len(Enrollments.objects.filter(course__in = courses))
    announcementsNum = len(Announcement.objects.filter(course__in = courses))
    feedbaksNum = len(Feedback.objects.filter(user=request.user))
    return render(request, 'collegeManagement/staff/staffHome.html', 
    {"coursesNum":coursesNum, "lecturesNum":lecturesNum, "studentsNum":studentsNum, "announcementsNum":announcementsNum, "feedbaksNum":feedbaksNum
    })

# courses
def teachedCourses(request):
    teached_courses = Course.objects.filter(staff=Staffs.objects.get(admin=request.user))
    return render(request, 'collegeManagement/staff/teachedCourses.html',{"teached_courses":teached_courses})

def courseView(request, cid):
    print(cid)
    return render(request, 'collegeManagement/staff/courseView.html',{"cid":cid})

def staffLectures(request,cid):
    course_lectures = Lecture.objects.filter(course=Course.objects.get(id=cid)).order_by("-created_at")
    return render(request, 'collegeManagement/staff/staffLectures.html', {"course_lectures":course_lectures,"cid":cid})

def addLecture(request,cid):
    if request.method == 'POST':
        file = ""
        original_name=""
        if 'file' in request.FILES:
            file = request.FILES['file']
            original_name = file.name
            now = datetime.datetime.now()
            dt_string = now.strftime("%d%m%Y%H%M%S")
            print("date and time =", dt_string)
            file.name = dt_string+"."+(file.name).split(".")[1]
        else:
            print("error")
            return redirect('../../staffLectures/'+str(cid))
        
        course = Course.objects.get(id=cid)
        lecture = Lecture(course=course, file=file, original_name=original_name , name=file.name)
        lecture.save()
        return redirect('../../staffLectures/'+str(cid))

def announcements(request,cid):
    course_announcements = Announcement.objects.filter(course=Course.objects.get(id=cid)).order_by("-created_at")
    return render(request, 'collegeManagement/staff/announcements.html', {"course_announcements":course_announcements,"cid":cid})


def addAnnouncement(request,cid):
    if request.method == 'POST':
        announce = request.POST["announcement"]
        course = Course.objects.get(id=cid)
        announcement = Announcement(course=course, announcement=announce)
        announcement.save()
        return redirect('../../announcements/'+str(cid))

def viewCourses(request):
    courses = Course.objects.all()
    return render(request, 'collegeManagement/staff/courses.html', {"courses":courses})


# enrollment Requests
def enrollmentRequests(request):
    courses = Course.objects.filter(staff=Staffs.objects.get(admin=request.user))
    requests = EnrollmentRequests.objects.filter(course__in = courses)
    print("courses: ")
    print(requests)
    return render(request, 'collegeManagement/staff/enrollmentRequests.html', {"requests":requests})

# accept Request
def acceptReq(request, rid):
    request = EnrollmentRequests.objects.get(id=rid)
    enrollment = Enrollments(student=request.student, course=request.course)
    enrollment.save()
    request.delete()
    return redirect('../../enrollmentRequests')

# accept Request
def rejectReq(request, rid):
    request = EnrollmentRequests.objects.get(id=rid)
    request.delete()
    return redirect('../../enrollmentRequests')

# accept all
def acceptAllenrollments(request):
    for r in EnrollmentRequests.objects.all():
        enrollment = Enrollments(student=r.student, course=r.course)
        enrollment.save()
        r.delete()
    return redirect('../../enrollmentRequests')


# feedback
def feedback(request):
    if request.method == 'POST':
        feedback = Feedback(feedback=request.POST["feedback"], user=request.user)
        feedback.save()
        return redirect('feedback')
    feedback_reply=[]
    feedbacks = Feedback.objects.filter(user=request.user).order_by("-created_at")
    for f in feedbacks:
        try:
            reply = Reply.objects.get(feedback=f)
            feedback_reply.append([f, reply.reply])
        except Reply.DoesNotExist:
            feedback_reply.append([f, "No Reply"])
    return render(request, 'collegeManagement/staff/feedback.html', {"feedbacks":feedback_reply})

# apply for leave
def leave(request):
    if request.method == 'POST':
        request = LeaveRequest(reason=request.POST["reason"], user=request.user)
        request.save()
        return redirect('leave')
    return render(request, 'collegeManagement/staff/leave.html', {})

# quizes
def quizes(request, cid):
    quizes = Quiz.objects.filter(course = Course.objects.get(id=cid))
    return render(request, 'collegeManagement/staff/quizes.html', {"cid":cid, "quizes":quizes})

# add Quiz
def addQuiz(request, cid):
    return render(request, 'collegeManagement/staff/makequize.html', {"cid":cid})

@csrf_exempt
def submitQuiz(request):
    if request.method == "POST":
        data = json.loads(request.body)
        quiz = Quiz()
        quiz.course =  Course.objects.get(id=data.get("cid"))
        quiz.save()
        questions = data.get("questions")
        print(questions)
        for question in questions:
            q = Question()
            q.quiz = quiz
            q.question = question[0]
            q.right = question[2]
            q.save()
            print(q.question)
            for option in question[1]:
                opn = Option()
                opn.question = q
                opn.option = option
                opn.save()
                print(opn.option)
        return JsonResponse({"success": "The Quiz has been added successfully"}, status=400)


def showQuiz(request, qid):
    quiz = Quiz.objects.get(id = qid)
    questions = Question.objects.filter(quiz=quiz)
    questions_options = []
    for question in questions:
        questions_options.append([question, Option.objects.filter(question=question)])
    return render(request, 'collegeManagement/staff/showQuiz.html', {"qid":qid,"questions":questions_options})


# appointements
def appointements(request, cid):
    if request.method == 'POST':
        course = Course.objects.get(id=cid)
        freq = int(request.POST["freq"])
        title = request.POST["title"]
        # parse time
        time = request.POST["time"]
        timeArr = time.split(":")
        t = datetime.time(int(timeArr[0]), int(timeArr[1]), int(timeArr[2]))
        print(t)
        appoint = apointement(title=title, course=course, time=t, frequency=freq)
        appoint.save()
        return redirect("../appointements/"+str(cid))
    appointements = apointement.objects.filter(course = Course.objects.get(id=cid)).order_by("-created_at")
    return render(request, 'collegeManagement/staff/appointements.html', 
    {"cid":cid, "appointements":appointements})

    

