# bassant1999
# college management system
## installations
django_cryptography library using **pip install django-cryptography**,
django_cryptography library is used in encryption and decryption.

## introduction
the web site consists of three types of users which are 
1. Head Of Department(HOD)or admin
2. student
3. staff
to start, create a superuser that will act as **Head Of Department(HOD)or admin**.
## getting start
1. run **pip freeze > requirement.txt**
2. run **python manage.py makemigrations**, and run **python manage.py migrate**
3. create a superuser that will act as Head Of Department(HOD)or admin using **python manage.py createsuperuser** (where you choose username, and password of the user).
4. run **python manage.py runserver**

## description
the web site contains a **Head Of Department(HOD)or admin page, student page, and staff page**
1. **functionalities in Head Of Department(HOD)or admin page**:
   - HOD (admin) handles the join requests from staff or students (HOD accepts or rejects the join requests)
   - HOD (admin) handles the leave requests from staff or students (HOD accepts or rejects the leave requests)
   - HOD page displays the students' details
   - HOD (admin) can edit, delete or add any student
   - HOD page displays the results of the students
   - HOD page displays the staff details
   - HOD (admin) can edit, delete or add any staff
   - HOD page displays the courses' details
   - HOD (admin) can edit, delete or add any course where each course has code, name, and is taught by one staff member.
   - HOD page displays all the student feedbacks and can reply to them
   - HOD page displays all the staff feedbacks and can reply to them

2. **functionalities in student page**:
   - the student can request to enroll in certain course, and this enrollment request can be accepted or rejected by the staff member who teach this course.
   - student page displays the courses that this student enrolls in them (in My Courses area).
   - student can view the course where each course contains lectures, announcements, and quizzes; lectures page contains the lectures' files that are loaded by the staff member who teach this course, announcements page contains the announcements that are put by the staff member who teach this course, and quizzes page contains the quizes that are loaded by the staff member who teach this course (note the student can take the quiz for only one time).
   - student page displays the results of the student in the quizzes
   - student can unenroll from a course.
   - student page displays all the courses (the courses that the student still does not request to enroll in them or still does not enrolled for them)
   - student page displays all the announcements
   - student can apply for leave.
   - student can send feedback, the student page shows all the feedbacks that have been sent by this student, and reply to these feedbacks.
   
3. **functionalities of staff page**:
   - staff enrollment request of students requesting the courses that this staff member teach (the staff accepts or rejects the enrollment requests).
   - staff page displays the courses that this staff teach (in My courses area).
   - staff can view the course where each course contains lectures, announcements, and quizzes; staff can add lectures files, announcements, and make quizzes (by adding the questions, and the options) in the course
   - staff page displays all the courses.
   - staff can apply for leave.
   - staff can send feedback, the staff page shows all the feedbacks that have been sent by this student, and reply to these feedbacks.
  
4. HOD page, student page, and staff page contains simple text chat where users can chat with each other to help each others.
5. HOD page, student page, and staff page contains search mechanism where user can search for a user, course, or chat.
