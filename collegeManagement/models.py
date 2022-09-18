from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
	HOD = '1'
	STAFF = '2'
	STUDENT = '3'
	
	EMAIL_TO_USER_TYPE_MAP = {
		'hod': HOD,
		'staff': STAFF,
		'student': STUDENT
	}

	user_type_data = ((HOD, "HOD"), (STAFF, "Staff"), (STUDENT, "Student"))
	user_type = models.CharField(default=1, choices=user_type_data, max_length=10)

	def serialize(self):
		return {
			"id": self.id,
			"email":self.email,
			"username": self.username,
			"user_type":self.user_type
	}


class AdminHOD(models.Model):
	id = models.AutoField(primary_key=True)
	admin = models.OneToOneField(User, on_delete = models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = models.Manager()


class Staffs(models.Model):
	id = models.AutoField(primary_key=True)
	admin = models.OneToOneField(User, on_delete = models.CASCADE)
	address = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = models.Manager()


class Students(models.Model):
	id = models.AutoField(primary_key=True)
	admin = models.OneToOneField(User, on_delete = models.CASCADE)
	gender = models.CharField(max_length=50)
	GPA =  models.DecimalField(max_digits=5,decimal_places=2, null=True)
	profile_pic = models.FileField()
	address = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = models.Manager()

class Request(models.Model):
	username = models.CharField(max_length=64)
	email = models.CharField(max_length=64)
	password = models.CharField(max_length=64)
	user_type = models.IntegerField()
	first_name= models.CharField(max_length=64)
	last_name= models.CharField(max_length=64)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
class Course(models.Model):
	name = models.CharField(max_length=64)
	code = models.CharField(max_length=64)
	staff = models.ForeignKey(Staffs, on_delete=models.CASCADE, related_name="staff")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	def serialize(self):
		return {
			"id": self.id,
			"name":self.name,
			"code": self.code
			}

class Enrollments(models.Model):
	student = models.ForeignKey(Students, on_delete=models.CASCADE, related_name="student")
	course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class EnrollmentRequests(models.Model):
	student = models.ForeignKey(Students, on_delete=models.CASCADE, related_name="rstudent")
	course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="rcourse")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Chat(models.Model):
	user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user1", null=True)
	user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2", null=True)
	new = models.IntegerField( default= 1)

class Message(models.Model):
	sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
	reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reciever")
	chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="chat")
	message = models.CharField(max_length=800,null=True)
	file = models.FileField(upload_to='files/',null=True)
	original_name = models.CharField(max_length=64 ,null=True)
	name = models.CharField(max_length=64 ,null=True)
	read = models.IntegerField( default= 0)
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True)
	def serialize(self):
		return {
			"id": self.id,
			"message":self.message
	}

class Lecture(models.Model):
	course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lcourse")
	file = models.FileField(upload_to='lectures/',null=True)
	original_name = models.CharField(max_length=64 ,null=True)
	name = models.CharField(max_length=64 ,null=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True)

class Announcement(models.Model):
	course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="Acourse",null=True)
	announcement = models.CharField(max_length=64 ,null=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True)

class Feedback(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="fUser")
	feedback = models.CharField(max_length=600 ,null=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True)

class Reply(models.Model):
	feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, related_name="rfeedback")
	reply = models.CharField(max_length=600 ,null=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True)

class LeaveRequest(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="LRUser")
	reason = models.CharField(max_length=600 ,null=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True)


class Quiz(models.Model):
	course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="qCourse")
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True)


class Question(models.Model):
	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="quiz")
	question = models.CharField(max_length=600 ,null=True)
	right = models.CharField(max_length=400 ,null=True)


class Option(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="quetion")
	option = models.CharField(max_length=400 ,null=True)


class Result(models.Model):
	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="rquiz")
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rUser")
	result = models.DecimalField(max_digits=5,decimal_places=2, null=True)
	total = models.DecimalField(max_digits=5,decimal_places=2, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class apointement(models.Model):
	title = models.CharField(max_length=100 ,null=True)
	course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="apCourse")
	time = models.TimeField()
	# strTime =  models.CharField(max_length=100 ,null=True)
	frequency = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)