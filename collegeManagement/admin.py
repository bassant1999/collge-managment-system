from django.contrib import admin


from xml.etree.ElementTree import Comment
from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Students)
admin.site.register(Staffs)
admin.site.register(Request)
admin.site.register(Course)
admin.site.register(Enrollments)
admin.site.register(EnrollmentRequests)
admin.site.register(Chat)
admin.site.register(Message)
admin.site.register(Lecture)
admin.site.register(LeaveRequest)
admin.site.register(Announcement)
admin.site.register(Feedback)
admin.site.register(Reply)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Result)
admin.site.register(apointement)