document.addEventListener('DOMContentLoaded', function() {

  });


// register
function register(){
    const username = document.querySelector('#register-username').value;
    const fname = document.querySelector('#register-fname').value;
    const lname = document.querySelector('#register-lname').value;
    const email = document.querySelector('#register-email').value;
    const pwd = document.querySelector('#register-pwd').value;
    const conpwd = document.querySelector('#register-conpwd').value;
    const type = document.querySelector('#register-type').value;
    fetch('../doRegistration', {
        method: 'POST',
        body: JSON.stringify({
            username: username,
            first_name: fname,
            last_name:lname,
            email: email,
            password: pwd,
            confirmPassword: conpwd,
            type: type
        })
        })
        .then(response => response.json())
        .then(result => {
            if(result['error']) {
                document.querySelector('#register-messages').innerHTML = `<div class="alert alert-danger" role="alert">${result['error']}</div>`;
            }
            if(result['success']) {
                document.querySelector('#register-messages').innerHTML = `<div class="alert alert-success" role="alert">${result['success']}</div>`;
            }
        });
    return false;
}

// login
function login(){
    const email = document.querySelector('#login-email').value;
    const pwd = document.querySelector('#login-pwd').value;
    fetch('/doLogin', {
        method: 'POST',
        body: JSON.stringify({
            email: email,
            password: pwd
        })
        })
        .then(response => response.json())
        .then(result => {
            if(result['error']) {
                document.querySelector('#login-messages').innerHTML = `<div class="alert alert-danger" role="alert">${result['error']}</div>`;
            }
            if(result['success']) {
                if(result['success'] == "1"){
                    window.location.href = "../HODHome";
                }
                else if(result['success'] == "2"){
                    window.location.href = "../staffHome";
                }
                else{
                    window.location.href = "../studentHome";
                }
            }
        });
    return false;
}



  function search(name){
    // send 
    fetch('/search/'+name)
            .then(response => response.json())
            .then(result => {
                document.querySelector('.list-group').innerHTML="";
                const ulNode = document.createElement("ul");
                for (let i = 0; i < result.length; i++) {
                    const aNode = document.createElement("a");
                    aNode.href = `/chat/${result[i].id}`;
                    const liNode = document.createElement("li");
                    liNode.innerHTML = `${result[i].username} (${result[i].email})`
                    aNode.appendChild(liNode);
                    ulNode.appendChild(aNode);
                    // document.querySelector('.list-group').innerHTML += `<a href="/chat/${result[i].id}" style="padding:10px;"><li>${result[i].username} (${result[i].email})</li></a>`;
                }
                document.querySelector('.list-group').appendChild(ulNode);
                if(result['success']) {
                    alert(result['success']);
                }
            });
}



function searchCourse(name){
    // send 
    fetch('/searchCourse/'+name)
    .then(response => response.json())
    .then(result => {
        document.querySelector('.list-group').innerHTML="";
        const ulNode = document.createElement("ul");
        for (let i = 0; i < result.length; i++) {
            const aNode = document.createElement("a");
            aNode.href = `/showCourse/${result[i].id}`;
            const liNode = document.createElement("li");
            liNode.innerHTML = `${result[i].name} (code: ${result[i].code})`
            aNode.appendChild(liNode);
            ulNode.appendChild(aNode);
            // document.querySelector('.list-group').innerHTML += `<a href="/chat/${result[i].id}" style="padding:10px;"><li>${result[i].username} (${result[i].email})</li></a>`;
        }
        document.querySelector('.list-group').appendChild(ulNode);
        if(result['success']) {
            alert(result['success']);
        }
    });
}

// search profile
function searchProfile(name){
    // send 
    fetch('/searchProfile/'+name)
    .then(response => response.json())
    .then(result => {
        document.querySelector('.list-group').innerHTML="";
        const ulNode = document.createElement("ul");
        for (let i = 0; i < result.length; i++) {
            const aNode = document.createElement("a");
            aNode.href = `/profile/${result[i].id}`;
            const liNode = document.createElement("li");
            liNode.innerHTML = `${result[i].username} (${result[i].email})`
            aNode.appendChild(liNode);
            ulNode.appendChild(aNode);
            // document.querySelector('.list-group').innerHTML += `<a href="/chat/${result[i].id}" style="padding:10px;"><li>${result[i].username} (${result[i].email})</li></a>`;
        }
        document.querySelector('.list-group').appendChild(ulNode);
        if(result['success']) {
            alert(result['success']);
        }
    });
}


// chat
function chat(){
    const list = document.querySelector('.chating');
    list.removeChild(list.lastElementChild);
    list.removeChild(list.lastElementChild);
    list.removeChild(list.lastElementChild);
    message = document.querySelector('#chat-message').value;
    id = document.querySelector('#chat-id').value;
    // send 
    fetch('/send_message', {
        method: 'POST',
        body: JSON.stringify({
            message: message,
            id: id
        })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
            if(result['error']) {
                document.querySelector('#send-error').innerHTML = `<div class="alert alert-danger" role="alert">${result['error']}</div>`;
            }
            if(result['message']) {
                const divNode = document.createElement("div");
                divNode.className = "left";
                divNode.innerHTML = result['message'].message;
                list.appendChild(divNode);
                list.innerHTML +="<br> <br> <br>";
                // list.appendChild(document.createElement("br"))
                // list.appendChild(document.createElement("br"))
                window.scrollTo(0, document.body.scrollHeight);
                document.querySelector('#chat-message').value = "";
            }
        });
    return false;
}



function edit(){
    const username = document.querySelector('#username').value;
    const fname = document.querySelector('#fname').value;
    const lname = document.querySelector('#lname').value;
    const email = document.querySelector('#email').value;
    const type = document.querySelector('#type').value;
    const id = document.querySelector('#id').value;
    const gpa = 0;
    if(type == 1){
        const gpa = document.querySelector('#gpa').value;
    }
    // send 
    fetch('../../edit/'+id+"/"+type, {
        method: 'POST',
        body: JSON.stringify({
            username: username,
            fname: fname,
            lname: lname,
            email: email,
            gpa: gpa
        })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
            if(result['error']) {
                document.querySelector('.messages').innerHTML = `<div class="alert alert-danger" role="alert">${result['error']}</div>`;
            }
            if(result['success']) {
                document.querySelector('.messages').innerHTML = `<div class="alert alert-success" role="alert">${result['success']}</div>`;
            }
        });

    return false;
}


function add_member(){
    const username = document.querySelector('#username1').value;
    const fname = document.querySelector('#fname1').value;
    const lname = document.querySelector('#lname1').value;
    const email = document.querySelector('#email1').value;
    const password = document.querySelector('#password1').value;
    const type = document.querySelector('#type1').value;
    // send 
    fetch('../addMember/'+type, {
        method: 'POST',
        body: JSON.stringify({
            username: username,
            fname: fname,
            lname: lname,
            email: email,
            password: password
        })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
            if(result['error']) {
                document.querySelector('.messages').innerHTML = `<div class="alert alert-danger" role="alert">${result['error']}</div>`;
            }
            if(result['success']) {
                document.querySelector('.messages').innerHTML = `<div class="alert alert-success" role="alert">${result['success']}</div>`;
            }
        });

    return false;
}

// add course

function add_course() {
    const course_name = document.querySelector('#course-name').value;
    const course_code = document.querySelector('#course-code').value;
    const staff_email = document.querySelector('#staff-email').value;
    // send 
    fetch('/addCourse', {
        method: 'POST',
        body: JSON.stringify({
            name: course_name,
            code: course_code,
            email: staff_email
        })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
            if(result['error']) {
                document.querySelector('#add-course-messages').innerHTML = `<div class="alert alert-danger" role="alert">${result['error']}</div>`;
            }
            if(result['success']) {
                document.querySelector('#add-course-messages').innerHTML = `<div class="alert alert-success" role="alert">${result['success']}</div>`;
            }
        });

    return false;
  }

// enroll request
function enroll_request(){
    const course_name = document.querySelector('#course-enroll-name').value;
    const course_code = document.querySelector('#course-enroll-code').value;
    // send 
    fetch('../enrollment', {
        method: 'POST',
        body: JSON.stringify({
            name: course_name,
            code: course_code
        })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
            if(result['error']) {
                document.querySelector('#course-enroll-messages').innerHTML = `<div class="alert alert-danger" role="alert">${result['error']}</div>`;
            }
            if(result['success']) {
                document.querySelector('#course-enroll-messages').innerHTML = `<div class="alert alert-success" role="alert">${result['success']}</div>`;
            }
        });

    return false;
}

// reply
function reply(element){
    element.style.display="none";
    element.parentElement.children[0].style.display="block";
}
function feedback_reply(element){
    const reply = element.children[0].value;
    const id = element.children[2].value;;
    fetch('../../feedbackReply/'+id, {
        method: 'POST',
        body: JSON.stringify({
            reply:reply
        })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
            if(result['error']) {
                document.querySelector('.messages').innerHTML = `<div class="alert alert-danger" role="alert">${result['error']}</div>`;
            }
            if(result['success']) {
                element.parentElement.children[1].style.display="block";
                element.parentElement.children[1].style.width = "fit-content"
                element.parentElement.children[0].style.display="none";
                // document.querySelector('.messages').innerHTML = `<div class="alert alert-success" role="alert">${result['success']}</div>`;
            }
        });

    return false;

}

// add question
function add_question(){
    document.querySelector('#add-question').style.display="none";
    document.querySelector('#question').style.display="block";
}
let counter = 1;
let option_counter = 1;
let c= 1;
var questions = [];
var options = []
var question_head = "";
var right_answer = "";

function add_question_head(){
    const question =  document.querySelector('#question-head').value;
    // alert(question);
    // alert(counter);
    const divNode = document.createElement("div");
    const pNode = document.createElement("p");
    pNode.innerHTML = `<strong>Quetion ${counter}</strong> ${question}:`;
    divNode.appendChild(pNode);
    document.querySelector('#questions').appendChild(divNode)
    document.querySelector('#question').style.display="none";
    document.querySelector('#option').style.display="block";
    document.querySelector('#right-answer-message').innerHTML = "";
    question_head = question;
    // alert(question_head);
    return false;
}

function add_option(){
    option =  document.querySelector('#question-option').value;
    // alert("hi");
    // alert(option_counter);
    // alert(option+""+option_counter.toString(10)+" "+c.toString(10));
    const inputNode = document.createElement("input");
    inputNode.type = "radio";
    inputNode.name = option_counter.toString(10);
    inputNode.id = c.toString(10);
    inputNode.value = option;
    const labelNode = document.createElement("label");
    labelNode.for = c.toString(10);
    labelNode.innerHTML = option;
    c++;
    length = (document.querySelector('#questions').children).length;
    last = document.querySelector('#questions').children[length-1];
    last.appendChild(inputNode);
    last.appendChild(labelNode);
    last.innerHTML +="<br>";
    // alert(last.children[0].innerHTML);
    // alert(c);
    options.push(option);
    // alert(options);
    return false;
}

function save_question(){
    if(document.querySelector('#question-right-answer').value){
        // alert("hey");
        counter++;
        option_counter++;
        // alert(counter);
        // alert(option_counter);
        // alert(c);
        document.querySelector('#add-question').style.display="block";
        document.querySelector('#option').style.display="none";
        document.querySelector('#submit-quiz').style.display="block";
        questions.push([question_head, options, document.querySelector('#question-right-answer').value]);
        // alert(questions);
        options = [];
        question_head = "";
    }
    else{
        document.querySelector('#right-answer-message').innerHTML = `<div class="alert alert-danger" role="alert">please type the right answer</div>`
    }
}

function submit_question(){
    fetch('../../submitQuiz', {
        method: 'POST',
        body: JSON.stringify({
            questions:questions,
            cid:  document.querySelector('#quiz-cid').value
        })
        })
    .then(response => response.json())
    .then(result => {
        if(result['error']) {
           
        }
        if(result['success']) {
            window.alert(result['success']);
            window.location.href='../../addQuiz/'+(document.querySelector('#quiz-cid').value).toString(10);
        }
    });
}