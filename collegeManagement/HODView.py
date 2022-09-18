# from curses.ascii import US
from django.shortcuts import render,HttpResponse, redirect,HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login

from collegeManagement.studentView import results

# from collegeManagement.studentView import courses
from .models import User, Staffs, Students, AdminHOD
from django.contrib import messages
from .models import *
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.db.models import Q

# Home
def HODHome(request):
	# new
	user = request.user
	chatsNum = len(Chat.objects.filter(Q(user1=user, new = 1) | Q(user2=user, new = 1)))
	messagesNum = len(Message.objects.filter(reciever=user, read=0))
	# end
	studentsNum = len(Students.objects.all())
	staffsNum = len(Staffs.objects.all())
	coursesNum = len(Course.objects.all())
	requestsNum = len(Request.objects.all())
	return render(request, 'collegeManagement/hod/HODHome.html', 
	{"studentsNum":studentsNum, "staffsNum":staffsNum, "coursesNum":coursesNum, "requestsNum":requestsNum, "chatsNum":chatsNum, "messagesNum": messagesNum }
	)

# students request to join
def studentJoin(request):
	students = Request.objects.filter(user_type=1).order_by('-created_at')
	return render(request, 'collegeManagement/hod/studentJoin.html', {"students":students})

def accept(request, rid, type):
	member = Request.objects.get(id=rid)
	print(member.username)
	user_type = User.STAFF
	if type == 1:
		user_type = User.STUDENT
	# add to users and students tables
	user = User()
	user.username = member.username
	user.email = member.email
	user.password = make_password(member.password)
	user.user_type = user_type
	user.first_name = member.first_name
	user.last_name = member.last_name
	user.save()
	if type == 1:
		Students.objects.create(admin=user)
	else:
		Staffs.objects.create(admin=user)
	#delete the request
	member.delete()
	# messages.add_message(request, messages.SUCCESS, 'accepted successfully.')
	if type == 1:
		return redirect("studentJoin")
	return redirect("staffJoin")

def reject(request, rid, type):
	member = Request.objects.get(id=rid)
	#delete the request
	member.delete()
	if type == 1:
		return redirect("studentJoin")
	return redirect("staffJoin")

def acceptAll(request, type):
	if type == 1:
		requests = Request.objects.filter(user_type = 1)
		for member in requests:
			user = User()
			user.username = member.username
			user.email = member.email
			user.password = make_password(member.password)
			user.user_type = User.STUDENT
			user.first_name = member.first_name
			user.last_name = member.last_name
			user.save()
			Students.objects.create(admin=user)
			member.delete()
	else:
		requests = Request.objects.filter(user_type = 0)
		for member in requests:
			user = User()
			user.username = member.username
			user.email = member.email
			user.password = make_password(member.password)
			user.user_type = User.STAFF
			user.first_name = member.first_name
			user.last_name = member.last_name
			user.save()
			Staffs.objects.create(admin=user)
			member.delete()
	if type == 1:
		return redirect("studentJoin")
	return redirect("staffJoin")

# staff request to join
def staffJoin(request):
	staff = Request.objects.filter(user_type=0)
	return render(request, 'collegeManagement/hod/staffJoin.html',{"staff":staff})


# diplay students
def studentDisplay(request):
	students = Students.objects.all()
	return render(request, 'collegeManagement/hod/studentDisplay.html',{"students":students})

# add Student
@csrf_exempt
def addMember(request, type):
	if request.method == "POST":
		data = json.loads(request.body)
		username = data.get("username")
		fname = data.get("fname")
		lname = data.get("lname")
		email = data.get("email")
		password = data.get("password")
		if not (username and fname and lname and email and password):
			return JsonResponse({"error": "Please provide all the details!!"}, status=400)

		is_user_exists = User.objects.filter(email=email).exists()

		if is_user_exists:
			return JsonResponse({"error": "User with this email id already exists"}, status=400)

		is_user_exists = User.objects.filter(username=username).exists()

		if is_user_exists:
			return JsonResponse({"error": "User with this Username already exists"}, status=400)

		is_user_exists = Request.objects.filter(email=email).exists()

		if is_user_exists:
			return JsonResponse({"error": "User with this email id already exists"}, status=400)

		is_user_exists = Request.objects.filter(username=username).exists()

		if is_user_exists:
			return JsonResponse({"error": "User with this Username already exists"}, status=400)
		
		
		if type == 1:
			user = User(username=username, first_name=fname, last_name=lname, email=email, password=password , user_type=User.STUDENT)
			user.save()
			student = Students(admin=user)
			student.save()
		else:
			user = User(username=username, first_name=fname, last_name=lname, email=email, password=password , user_type=User.STAFF)
			user.save()
			staff = Staffs(admin=user)
			staff.save()
		return JsonResponse({"success": "added succesfully"}, status=400)
	return render(request, 'collegeManagement/hod/addMember.html', {"type":type})

# staff Display
def staffDisplay(request):
	staffs = Staffs.objects.all()
	return render(request, 'collegeManagement/hod/staffDisplay.html', {"staffs":staffs})

# feedback
def feedback(request, type):
	studentfeedbacks =  []
	stafffeedbacks =  []
	for f in Feedback.objects.all().order_by("-created_at"):
		if f.user.user_type == User.STUDENT:
			studentfeedbacks.append(f)
		elif f.user.user_type == User.STAFF:
			stafffeedbacks.append(f)
	
	print(studentfeedbacks)
	print(stafffeedbacks)
	feedbacks = []
	if type == 1:
		feedbacks = studentfeedbacks
	else:
		feedbacks = stafffeedbacks
	return render(request, 'collegeManagement/hod/feedback.html', {"feedbacks":feedbacks})

@csrf_exempt
def feedbackReply(request, id):
	if request.method == "POST":
		data = json.loads(request.body)
		reply = data.get("reply")
		feedback = Feedback.objects.get(id=id)
		reply = Reply(feedback = feedback , reply = reply)
		reply.save()
		return JsonResponse({"success": "added succesfully"}, status=400)


# courses
def coursesDisplay(request):
	courses = Course.objects.all()
	return render(request, 'collegeManagement/hod/coursesDisplay.html',{"courses":courses})

@csrf_exempt
def addCourse(request):
	if request.method == "POST":
		data = json.loads(request.body)
		name = data.get("name")
		code = data.get("code")
		email = data.get("email")
		is_user_exists = User.objects.filter(email=email).exists()
		if not is_user_exists:
			return JsonResponse({"error": "this email does not exist"}, status=400)
		is_code_exists = Course.objects.filter(code=code).exists()
		if is_code_exists:
			return JsonResponse({"error": "this code is already exists"}, status=400)
		user = User.objects.get(email=email)
		staff = Staffs.objects.get(admin=user)
		course = Course(name=name,code=code,staff=staff)
		course.save()
		return JsonResponse({"success": "added succesfully"}, status=400)
	return render(request, 'collegeManagement/hod/addCourse.html')

# edit
@csrf_exempt
def edit(request, sid, type):
	if request.method == "POST":
		data = json.loads(request.body)
		username = data.get("username")
		fname = data.get("fname")
		lname = data.get("lname")
		email = data.get("email")
		gpa = data.get("gpa")
		if(type == 1):
			student = Students.objects.get(id=sid)
			student.GPA = gpa
			user = User.objects.get(id=student.admin.id)
			user.username = username
			user.first_name = fname
			user.last_name = lname
			user.email = email
			user.save(update_fields=['username', 'first_name', 'last_name', 'email'])
			student.admin = user
			student.save(update_fields=['admin', 'GPA'])
			return JsonResponse({"success": "edited succesfully"}, status=400)
		else:
			staff = Staffs.objects.get(id=sid)
			user = User.objects.get(id=staff.admin.id)
			user.username = username
			user.first_name = fname
			user.last_name = lname
			user.email = email
			user.save(update_fields=['username', 'first_name', 'last_name', 'email'])
			staff.admin = user
			staff.save(update_fields=['admin'])
			return JsonResponse({"success": "edited succesfully"}, status=400)
	member = ""
	if(type == 1):	
		member = Students.objects.get(id=sid)
	else:
		member = Staffs.objects.get(id=sid)
	print(member)
	return render(request, 'collegeManagement/hod/edit.html', {"member":member, "type":type})

# delete
def delete(request, sid, type):
	if type == 1:
		user = Students.objects.get(id=sid).admin
		user.delete()
		return redirect("../../studentDisplay")
	else:
		user = Staffs.objects.get(id=sid).admin
		user.delete()
		return redirect("../../staffDisplay")

# display leave requests
def displayleaverequests(request, type):
	requests = LeaveRequest.objects.all()
	if type == 1:
		studentRequests = []
		for r in requests:
			if r.user.user_type == User.STUDENT:
				studentRequests.append(r)
		return render(request, 'collegeManagement/hod/displayleaverequests.html', {"requests":studentRequests})
	else:
		staffRequests = []
		for r in requests:
			if r.user.user_type == User.STAFF:
				staffRequests.append(r)
		return render(request, 'collegeManagement/hod/displayleaverequests.html', {"requests":staffRequests})


def acceptLeaveRequest(request, rid):
	req = LeaveRequest.objects.get(id=rid)
	user = req.user
	type=0
	print("here")
	if user.user_type == User.STUDENT:
		student = Students.objects.get(admin=user)
		student.delete()
		type = 1
		print("hete")
	else:
		staff = Staffs.objects.get(admin=user)
		staff.delete()
		type = 0
		print("hetet")
	req.delete()
	user.delete()
	print("hette")
	return redirect("../displayleaverequests/"+str(type))


def rejectLeaveRequest(request, rid):
	req = LeaveRequest.objects.get(id=rid)
	user = req.user
	type=0
	if user.user_type == User.STUDENT:
		type = 1
	else:
		type = 0
	req.delete()
	return redirect("../displayleaverequests/"+str(type))


# viewResults
def viewResults(request):
	results = Result.objects.all()
	return render(request, 'collegeManagement/hod/viewResults.html', {"results":results})