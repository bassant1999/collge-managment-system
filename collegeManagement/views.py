from asyncio.windows_events import NULL
from django.shortcuts import render,HttpResponse, redirect,HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
from .models import *
from django.contrib import messages
import json
from django.http import JsonResponse
from django.db.models import Q
from django.http import FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password

def index(request):
	# print(request.user.is_authenticated())
	if request.user.is_authenticated:
		if request.user.user_type == User.STUDENT:
			return redirect('studentHome')
		elif request.user.user_type == User.STAFF:
			return redirect('staffHome')
		elif request.user.user_type == User.HOD:
			return redirect('HODHome')
	return render(request, 'collegeManagement/login_page.html')


def contact(request):
	return render(request, 'collegeManagement/contact.html')


def loginUser(request):
	return render(request, 'collegeManagement/login_page.html')

@csrf_exempt
def doLogin(request):
	if request.method == "POST":
		data = json.loads(request.body)
		email_id = data.get("email")
		password = data.get("password")
		print("login")
		print(email_id)
		print(password)
		print("here")
		if not (email_id and password):
			return JsonResponse({"error": "Please provide all the details!!"}, status=400)
		try:
			print("here")
			user = User.objects.get(email=email_id)
			print("password: ")
			print(user.password)
			print(password)
			print(check_password(password, user.password))
			if(check_password(password, user.password)):
				login(request, user)
				print("user: ")
				print(user.user_type)

				if user.user_type == User.STUDENT:
					# return redirect('studentHome')
					return JsonResponse({"success": "3"}, status=400)
				elif user.user_type == User.STAFF:
					# return redirect('staffHome')
					return JsonResponse({"success": "2"}, status=400)
				elif user.user_type == User.HOD:
					# return redirect('HODHome')
					return JsonResponse({"success": "1"}, status=400)

			else:
				return JsonResponse({"error": "Password is wrong"}, status=400)

		except User.DoesNotExist:
			print("here2")
			return JsonResponse({"error": "the email is Wrong"}, status=400)

	return JsonResponse({"error": "invalid request"}, status=400)

	
def registration(request):
    return render(request, 'collegeManagement/register.html')
	
@csrf_exempt
def doRegistration(request):
	if request.method == "POST":
		data = json.loads(request.body)
		username = data.get("username")
		first_name = data.get("first_name")
		last_name = data.get("last_name")
		email_id = data.get("email")
		password = data.get("password")
		confirm_password = data.get("confirmPassword")
		user_type = data.get("type")
		print("method: ")
		print(request.method)
		print(username)
		print(email_id)
		print(password)
		print(confirm_password)
		print(first_name)
		print(last_name)
		if not (username and email_id and password and confirm_password):
			return JsonResponse({"error": "Please provide all the details!!"}, status=400)
	
		if password != confirm_password:
			return JsonResponse({"error": "Both passwords should match!!"}, status=400)

		is_user_exists = User.objects.filter(email=email_id).exists()

		if is_user_exists:
			return JsonResponse({"error": "User with this email id already exists. Please proceed to login!!"}, status=400)

		is_user_exists = Request.objects.filter(email=email_id).exists()

		if is_user_exists:
			return JsonResponse({"error": "User with this email id already exists. Please proceed to login!!"}, status=400)

		if user_type is None:
			return JsonResponse({"error": "Please provide type for the account"}, status=400)

		if User.objects.filter(username=username).exists():
			return JsonResponse({"error": "User with this username already exists. Please use different username"}, status=400)
	
		if Request.objects.filter(username=username).exists():
			return JsonResponse({"error": "User with this username already exists. Please use different username"}, status=400)


		request = Request()
		request.username = username
		request.email = email_id
		request.password = password
		request.user_type = user_type
		request.first_name = first_name
		request.last_name = last_name
		request.save()
		return JsonResponse({"success": "Your request has been sent successfully, please wait until HOD accept the request"}, status=400)
	return JsonResponse({"error": "invalid request"}, status=400)
	
def logout_user(request):
	logout(request)
	return HttpResponseRedirect('/')

# chats
def chats(request):
	user = request.user
	chats = Chat.objects.filter(Q(user1=user) | Q(user2=user))
	chats_messages = []
	for chat in chats:
		messages = Message.objects.filter(Q(sender=chat.user1, reciever=chat.user2) | Q(sender=chat.user2, reciever=chat.user1)).order_by('created_at')
		print(messages[len(messages) - 1])
		chats_messages.append([chat,messages[len(messages) - 1]])
	print(chats_messages)
	return render(request, 'collegeManagement/chats.html',{"chats_messages":chats_messages})

def chat(request,uid):
	sender = request.user
	reciever = User.objects.get(id=uid)
	messages=[]
	try:
		chat = Chat.objects.get(Q(user1=sender, user2=reciever) | Q(user1=reciever, user2=sender))
		messages = Message.objects.filter(chat=chat)
		print(messages)
		print("found")
		return render(request, 'collegeManagement/chat.html',{"reciever":reciever, "messages":messages})
	except Chat.DoesNotExist:
		print("chats")
		return render(request, 'collegeManagement/chat.html',{"reciever":reciever, "messages":messages})

# search
def search(request,name):
	users = User.objects.filter(Q(username__contains=name) | Q(email__contains=name) | Q(first_name__contains=name) | Q(last_name__contains=name))
	print(users)
	return JsonResponse([user.serialize() for user in users], safe=False)

# send message
@csrf_exempt
def send_message(request):
	if request.method == "POST":
		data = json.loads(request.body)
		message = data.get("message")
		# file = data.get("file")
		id = data.get("id")
		print(message)
		# print(file)
		print(id)
		sender = request.user
		reciever = User.objects.get(id=id)
		chat=""
		new_message = ""
		try:
			chat = Chat.objects.get(Q(user1=sender, user2=reciever) | Q(user1=reciever, user2=sender))
		except Chat.DoesNotExist:
			chat = Chat(user1=sender, user2=reciever)
			chat.save()
		if(message):
			new_message = Message(sender=sender, reciever=reciever, chat=chat, message=message)
			new_message.save()
		else:
			return JsonResponse({"error": "should send a message"}, status=400)
		return JsonResponse({"message": new_message.serialize()}, status=400)

from datetime import datetime

def send(request):
	if request.method == 'POST':
		message = request.POST["message"]
		file = ""
		original_name=""
		reciver_id = request.POST["id"]
		sender = request.user
		reciever = User.objects.get(id=reciver_id)
		if 'file' in request.FILES:
			file = request.FILES['file']
			original_name = file.name
			now = datetime.now()
			dt_string = now.strftime("%d%m%Y%H%M%S")
			print("date and time =", dt_string)
			file.name = dt_string+"."+(file.name).split(".")[1]
		print(message)
		print(reciver_id)
		chat=""
		try:
			chat = Chat.objects.get(Q(user1=sender, user2=reciever) | Q(user1=reciever, user2=sender))
		except Chat.DoesNotExist:
			chat = Chat(user1=sender, user2=reciever)
			chat.save()
		if(file and message):
			new_message = Message(sender=sender, reciever=reciever, chat=chat, message=message, file=file, original_name=original_name, name=file.name)
			new_message.save()
		elif(file and not message):
			new_message = Message(sender=sender, reciever=reciever, chat=chat, message=NULL, file=file, original_name=original_name, name=file.name)
			new_message.save()
		elif(not file and message):
			new_message = Message(sender=sender, reciever=reciever, chat=chat, message=message, file=NULL, original_name=original_name, name=NULL)
			new_message.save()
		else:
			return 'error'
		return redirect("../chat/"+str(reciver_id))

# upload
def upload(request, name, type):
	file=""
	if type == 1:
		file = open('media/files/'+str(name), 'rb')
	elif type == 2:
		file = open('media/lectures/'+str(name), 'rb')
	response = FileResponse(file)
	print(response)
	return response

# search Course
def searchCourse(request, name):
	courses = Course.objects.filter(Q(name__contains=name) | Q(code__contains=name))
	print(courses)
	return JsonResponse([course.serialize() for course in courses], safe=False)

# search Profile
def searchProfile(request, name):
	users = User.objects.filter(Q(username__contains=name) | Q(email__contains=name) | Q(first_name__contains=name) | Q(last_name__contains=name))
	print(users)
	return JsonResponse([user.serialize() for user in users], safe=False)

def profile(request, uid):
	user = User.objects.get(id=uid)
	if user.user_type == User.STUDENT:
		courses = Enrollments.objects.filter(student=Students.objects.get(admin=user))
		return render(request, 'collegeManagement/profile.html',{"puser":user, "courses":courses, "count":len(courses)})
	elif user.user_type == User.STAFF:
		courses = Course.objects.filter(staff= Staffs.objects.get(admin=user))
		return render(request, 'collegeManagement/profile.html',{"puser":user, "courses":courses, "count":len(courses)})
	elif user.user_type == User.HOD:
		return render(request, 'collegeManagement/profile.html',{"puser":user})

def viewCourse(request, cid):
	course = Course.objects.get(id=cid)
	staff_courses = Course.objects.filter(staff=course.staff)
	print(staff_courses)
	return render(request, 'collegeManagement/course.html',{"course":course, "staff_courses":staff_courses})
# bassant.student@eng.adu 56566565bass
# bassant.hod@eng.adu 123
# bosy.hod@eng.adu 123 hod