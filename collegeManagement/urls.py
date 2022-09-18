from django.urls import path
from django.contrib import admin
from django.urls import path, include
from . import views
from .import HODView, studentView, staffView

urlpatterns = [
    path("", views.index, name="index"),
    path('contact', views.contact, name="contact"),
    path('login', views.loginUser, name="login"),
    path('logout_user', views.logout_user, name="logout_user"),
    path('registration', views.registration, name="registration"),
    path('doLogin', views.doLogin, name="doLogin"),
    path('doRegistration', views.doRegistration, name="doRegistration"),
    path('chats', views.chats, name="chats"),
    path('chat/<int:uid>', views.chat, name="chat"),
    path('search/<str:name>', views.search, name="search"),
    path('send', views.send, name="send"),
    path('upload/<str:name>/<int:type>', views.upload, name="upload"),
    path('searchCourse/<str:name>', views.searchCourse, name="searchCourse"),
    path('showCourse/<int:cid>', views.viewCourse, name="showCourse"),
    path('searchProfile/<str:name>', views.searchProfile, name="searchProfile"),
    path('profile/<int:uid>', views.profile, name="profile"),
    path('send_message', views.send_message, name="send_message"),

    # students
    path('studentHome', studentView.studentHome, name="studentHome"),
    path('allCourses', studentView.allCourses, name="allCourses"),
    path('enrolledCourses', studentView.enrolledCourses, name="enrolledCourses"),
    path('enroll/<int:cid>', studentView.enroll, name="enroll"),
    path('unenroll/<int:cid>', studentView.unenroll, name="unenroll"),
    path('enrollment', studentView.enrollment, name="enrollment"),
    path('viewCourse/<int:cid>', studentView.viewCourse, name="viewCourse"),
    path('sannouncements/<int:cid>', studentView.sannouncements, name="sannouncements"),
    path('studentFeedback', studentView.studentFeedback, name="studentFeedback"),
    path('studentLeave', studentView.studentLeave, name="studentLeave"),
    path('allAnnouncements', studentView.allAnnouncements, name="allAnnouncements"),
    path('lectures/<int:cid>', studentView.lectures, name="slectures"),
    path('studentQuizes/<int:cid>', studentView.studentQuizes, name="studentQuizes"),
    path('studentShowQuiz/<int:qid>', studentView.studentShowQuiz, name="studentShowQuiz"),
    path('results', studentView.results, name="results"),
    path('studentAppointements/<int:cid>', studentView.studentAppointements, name="studentAppointements"),

    # HOD
    path('HODHome', HODView.HODHome, name="HODHome"),
    path('studentJoin', HODView.studentJoin, name="studentJoin"),
    path('accept/<int:rid>/<int:type>', HODView.accept, name="accept"), 
    path('acceptAll/<int:type>', HODView.acceptAll, name="acceptAll"), 
    path('reject/<int:rid>/<int:type>', HODView.reject, name="reject"), 
    path('staffJoin', HODView.staffJoin, name="staffJoin"),
    path('studentDisplay', HODView.studentDisplay, name="studentDisplay"),
    path('addMember/<int:type>', HODView.addMember, name="addMember"),
    path('staffDisplay', HODView.staffDisplay, name="staffDisplay"),
    # path('addStaff', HODView.addStaff, name="addStaff"), 
    # path('studentFeedback', HODView.studentFeedback, name="studentFeedback"), 
    # path('staffFeedback', HODView.staffFeedback, name="staffFeedback"), 
    path('coursesDisplay', HODView.coursesDisplay, name="coursesDisplay"), 
    path('addCourse', HODView.addCourse, name="addCourse"),  
    path('edit/<int:sid>/<int:type>', HODView.edit, name="edit"),
    path('delete/<int:sid>/<int:type>', HODView.delete, name="delete"),
    path('displayleaverequests/<int:type>', HODView.displayleaverequests, name="displayleaverequests"),
    path('acceptLeaveRequest/<int:rid>', HODView.acceptLeaveRequest, name="acceptLeaveRequest"),
    path('rejectLeaveRequest/<int:rid>', HODView.rejectLeaveRequest, name="rejectLeaveRequest"),
    path('feedback/<int:type>', HODView.feedback, name="feedback"),
    path('feedbackReply/<int:id>', HODView.feedbackReply, name="feedbackReply"),
    path('viewResults', HODView.viewResults, name="viewResults"),

    # Staff
    path('staffHome', staffView.staffHome, name="staffHome"),
    path('teachedCourses', staffView.teachedCourses, name="teachedCourses"),
    path('courseView/<int:cid>', staffView.courseView, name="courseView"),
    path('staffLectures/<int:cid>', staffView.staffLectures, name="staffLectures"),
    path('addLecture/<int:cid>', staffView.addLecture, name="addLecture"),
    path('announcements/<int:cid>', staffView.announcements, name="announcements"),
    path('addAnnouncement/<int:cid>', staffView.addAnnouncement, name="addAnnouncement"),
    path('enrollmentRequests', staffView.enrollmentRequests, name="enrollmentRequests"),
    path('acceptReq/<int:rid>', staffView.acceptReq, name="acceptReq"),
    path('rejectReq/<int:rid>', staffView.rejectReq, name="rejectReq"),
    path('acceptAllenrollments', staffView.acceptAllenrollments, name="acceptAllenrollments"),
    path('feedback', staffView.feedback, name="feedback"),
    path('leave', staffView.leave, name="leave"),
    path('viewCourses', staffView.viewCourses, name="viewCourses"),
    path('quizes/<int:cid>', staffView.quizes, name="quizes"),
    path('addQuiz/<int:cid>', staffView.addQuiz, name="addQuiz"),
    path('submitQuiz', staffView.submitQuiz, name="submitQuiz"),
    path('showQuiz/<int:qid>', staffView.showQuiz, name="showQuiz"),
    path('appointements/<int:cid>', staffView.appointements, name="appointements"),
    
    
]


# new
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)